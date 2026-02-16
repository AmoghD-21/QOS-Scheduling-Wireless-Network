import heapq

LINK_BANDWIDTH = 1_000_000  # 1 Mbps


# ==========================================================
# PRIORITY SCHEDULER
# ==========================================================

class PriorityScheduler:

    def __init__(self, buffer_size=50):

        self.buffer_size = buffer_size

        self.voice_queue = []
        self.video_queue = []
        self.data_queue = []

        self.current_time = 0

        self.transmitted_packets = []
        self.dropped_packets = []

        self.queue_history = []
        self.time_history = []

    # ------------------------------------------------------

    def add_packet(self, packet):

        if packet.traffic_type == "voice":
            if len(self.voice_queue) < self.buffer_size:
                self.voice_queue.append(packet)
            else:
                self.dropped_packets.append(packet)

        elif packet.traffic_type == "video":
            if len(self.video_queue) < self.buffer_size:
                self.video_queue.append(packet)
            else:
                self.dropped_packets.append(packet)

        else:
            if len(self.data_queue) < self.buffer_size:
                self.data_queue.append(packet)
            else:
                self.dropped_packets.append(packet)

    # ------------------------------------------------------

    def select_packet(self):

        if self.voice_queue:
            return self.voice_queue.pop(0)

        if self.video_queue:
            return self.video_queue.pop(0)

        if self.data_queue:
            return self.data_queue.pop(0)

        return None

    # ------------------------------------------------------

    def transmit(self, packet):

        waiting_time = self.current_time - packet.arrival_time

        if waiting_time > packet.deadline:
            self.dropped_packets.append(packet)
            return

        packet.start_time = self.current_time

        tx_time = packet.size / LINK_BANDWIDTH
        self.current_time += tx_time

        packet.end_time = self.current_time

        self.transmitted_packets.append(packet)

        total_q = (
            len(self.voice_queue) +
            len(self.video_queue) +
            len(self.data_queue)
        )

        self.queue_history.append(total_q)
        self.time_history.append(self.current_time)

    # ------------------------------------------------------

    def run(self, packets):

        packets.sort(key=lambda p: p.arrival_time)

        index = 0
        total_packets = len(packets)

        while index < total_packets or \
              self.voice_queue or self.video_queue or self.data_queue:

            while index < total_packets and \
                  packets[index].arrival_time <= self.current_time:

                self.add_packet(packets[index])
                index += 1

            packet = self.select_packet()

            if packet:
                self.transmit(packet)
            else:
                if index < total_packets:
                    self.current_time = packets[index].arrival_time
                else:
                    break


# ==========================================================
# WEIGHTED FAIR QUEUING (WFQ)
# ==========================================================

class WFQScheduler:

    def __init__(self, buffer_size=150):

        self.buffer_size = buffer_size

        self.virtual_time = 0
        self.heap = []

        self.current_time = 0

        self.transmitted_packets = []
        self.dropped_packets = []

        self.weights = {
            "voice": 5.0,
            "video": 3.0,
            "data": 1.0
        }

        self.MIN_WEIGHT = 0.5
        self.MAX_WEIGHT = 10.0

        self.last_finish = {
            "voice": 0,
            "video": 0,
            "data": 0
        }

        self.queue_history = []
        self.time_history = []

    # ------------------------------------------------------

    def add_packet(self, packet):

        if len(self.heap) >= self.buffer_size:
            self.dropped_packets.append(packet)
            return

        weight = self.weights[packet.traffic_type]

        start = max(self.virtual_time,
                    self.last_finish[packet.traffic_type])

        finish = start + (packet.size / weight)

        packet.finish_time = finish
        self.last_finish[packet.traffic_type] = finish

        heapq.heappush(self.heap, (finish, packet))

    # ------------------------------------------------------

    def transmit(self, packet):

        waiting_time = self.current_time - packet.arrival_time

        if waiting_time > packet.deadline:
            self.dropped_packets.append(packet)
            return

        packet.start_time = self.current_time

        tx_time = packet.size / LINK_BANDWIDTH
        self.current_time += tx_time

        packet.end_time = self.current_time

        self.virtual_time = self.current_time

        self.transmitted_packets.append(packet)

        delay = packet.end_time - packet.arrival_time

        if packet.traffic_type == "voice" and delay > 0.04:
            self.weights["voice"] *= 1.05

        elif packet.traffic_type == "video" and delay > 0.12:
            self.weights["video"] *= 1.03

        for key in self.weights:
            self.weights[key] = max(
                self.MIN_WEIGHT,
                min(self.weights[key], self.MAX_WEIGHT)
            )

        self.queue_history.append(len(self.heap))
        self.time_history.append(self.current_time)

    # ------------------------------------------------------

    def run(self, packets):

        packets.sort(key=lambda p: p.arrival_time)

        index = 0
        total_packets = len(packets)

        while index < total_packets or self.heap:

            while index < total_packets and \
                  packets[index].arrival_time <= self.current_time:

                self.add_packet(packets[index])
                index += 1

            if self.heap:
                _, packet = heapq.heappop(self.heap)
                self.transmit(packet)
            else:
                if index < total_packets:
                    self.current_time = packets[index].arrival_time
                else:
                    break


# ==========================================================
# PROPORTIONAL FAIR SCHEDULER
# ==========================================================

class PFScheduler:

    ALPHA = 0.9

    def __init__(self, buffer_size=150):

        self.buffer_size = buffer_size

        self.voice_queue = []
        self.video_queue = []
        self.data_queue = []

        self.current_time = 0

        self.transmitted_packets = []
        self.dropped_packets = []

        self.avg_throughput = {
            "voice": 1e-6,
            "video": 1e-6,
            "data": 1e-6
        }

        self.queue_history = []
        self.time_history = []

    # ------------------------------------------------------

    def add_packet(self, packet):

        total_queue_size = (
            len(self.voice_queue) +
            len(self.video_queue) +
            len(self.data_queue)
        )

        if total_queue_size >= self.buffer_size:
            self.dropped_packets.append(packet)
            return

        if packet.traffic_type == "voice":
            self.voice_queue.append(packet)
        elif packet.traffic_type == "video":
            self.video_queue.append(packet)
        else:
            self.data_queue.append(packet)

    # ------------------------------------------------------

    def select_packet(self):

        candidates = []

        if self.voice_queue:
            metric = LINK_BANDWIDTH / self.avg_throughput["voice"]
            candidates.append(("voice", metric))

        if self.video_queue:
            metric = LINK_BANDWIDTH / self.avg_throughput["video"]
            candidates.append(("video", metric))

        if self.data_queue:
            metric = LINK_BANDWIDTH / self.avg_throughput["data"]
            candidates.append(("data", metric))

        if not candidates:
            return None

        selected_class = max(candidates, key=lambda x: x[1])[0]

        if selected_class == "voice":
            return self.voice_queue.pop(0)
        elif selected_class == "video":
            return self.video_queue.pop(0)
        else:
            return self.data_queue.pop(0)

    # ------------------------------------------------------

    def transmit(self, packet):

        waiting_time = self.current_time - packet.arrival_time

        if waiting_time > packet.deadline:
            self.dropped_packets.append(packet)
            return

        packet.start_time = self.current_time

        tx_time = packet.size / LINK_BANDWIDTH
        self.current_time += tx_time

        packet.end_time = self.current_time

        self.transmitted_packets.append(packet)

        achieved_rate = packet.size / tx_time

        old_avg = self.avg_throughput[packet.traffic_type]

        self.avg_throughput[packet.traffic_type] = (
            self.ALPHA * old_avg +
            (1 - self.ALPHA) * achieved_rate
        )

        total_q = (
            len(self.voice_queue) +
            len(self.video_queue) +
            len(self.data_queue)
        )

        self.queue_history.append(total_q)
        self.time_history.append(self.current_time)

    # ------------------------------------------------------

    def run(self, packets):

        packets.sort(key=lambda p: p.arrival_time)

        index = 0
        total_packets = len(packets)

        while index < total_packets or \
              self.voice_queue or self.video_queue or self.data_queue:

            while index < total_packets and \
                  packets[index].arrival_time <= self.current_time:

                self.add_packet(packets[index])
                index += 1

            packet = self.select_packet()

            if packet:
                self.transmit(packet)
            else:
                if index < total_packets:
                    self.current_time = packets[index].arrival_time
                else:
                    break

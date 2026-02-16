# packet.py

class Packet:
    def __init__(self, packet_id, arrival_time, size, traffic_type):
        self.packet_id = packet_id
        self.arrival_time = arrival_time
        self.size = size  # in bits
        self.traffic_type = traffic_type

        # QoS parameters
        self.weight = self.assign_weight()
        self.deadline = self.assign_deadline()

        # Scheduling parameters
        self.finish_time = 0
        self.start_time = None
        self.end_time = None

    def assign_weight(self):
        if self.traffic_type == "voice":
            return 5
        elif self.traffic_type == "video":
            return 3
        else:
            return 1

    def assign_deadline(self):
        if self.traffic_type == "voice":
            return 0.05  # 50 ms
        elif self.traffic_type == "video":
            return 0.15  # 150 ms
        else:
            return 1.0  # 1 second

    def __repr__(self):
        return f"Packet(id={self.packet_id}, type={self.traffic_type}, arrival={self.arrival_time})"

# traffic_generator.py

import random
from packet import Packet


def generate_traffic(simulation_time, arrival_rate):
    """
    simulation_time: total simulation duration (seconds)
    arrival_rate: average packets per second
    """

    packets = []
    current_time = 0
    packet_id = 0

    while current_time < simulation_time:

        # Random inter-arrival time (Poisson-like)
        inter_arrival = random.expovariate(arrival_rate)
        current_time += inter_arrival

        if current_time > simulation_time:
            break

        # Random traffic type
        traffic_type = random.choice(["voice", "video", "data"])

        # Packet sizes (bits)
        if traffic_type == "voice":
            size = random.randint(500, 1000) * 8
        elif traffic_type == "video":
            size = random.randint(1000, 5000) * 8
        else:
            size = random.randint(5000, 10000) * 8

        packet = Packet(packet_id, current_time, size, traffic_type)
        packets.append(packet)

        packet_id += 1

    return packets

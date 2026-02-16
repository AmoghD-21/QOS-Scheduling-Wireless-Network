# metrics.py

from collections import defaultdict


def calculate_metrics(transmitted_packets, dropped_packets, simulation_time):

    stats = defaultdict(list)

    # Separate packets by type
    for p in transmitted_packets:
        delay = p.end_time - p.arrival_time
        stats[p.traffic_type].append(delay)

    results = {}

    total_bits = 0

    for traffic_type in ["voice", "video", "data"]:

        delays = stats[traffic_type]

        if delays:
            avg_delay = sum(delays) / len(delays)
        else:
            avg_delay = 0

        transmitted_count = len(delays)
        dropped_count = len([p for p in dropped_packets if p.traffic_type == traffic_type])

        loss_ratio = dropped_count / (transmitted_count + dropped_count) \
            if (transmitted_count + dropped_count) > 0 else 0

        results[traffic_type] = {
            "average_delay": avg_delay,
            "transmitted": transmitted_count,
            "dropped": dropped_count,
            "loss_ratio": loss_ratio
        }

    # Throughput
    for p in transmitted_packets:
        total_bits += p.size

    throughput = total_bits / simulation_time  # bits per second

    results["overall_throughput"] = throughput

    return results

def jains_fairness(transmitted_packets):

    throughput_per_type = defaultdict(int)

    for p in transmitted_packets:
        throughput_per_type[p.traffic_type] += p.size

    values = list(throughput_per_type.values())

    if not values:
        return 0

    numerator = (sum(values)) ** 2
    denominator = len(values) * sum(v ** 2 for v in values)

    if denominator == 0:
        return 0

    return numerator / denominator

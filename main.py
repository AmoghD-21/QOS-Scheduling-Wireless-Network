# main.py

from traffic_generator import generate_traffic
from scheduler import PriorityScheduler, WFQScheduler, PFScheduler
from metrics import calculate_metrics, jains_fairness
import matplotlib.pyplot as plt
import matplotlib.animation as animation


SIMULATION_TIME = 20
ARRIVAL_RATE = 120


def run_scheduler(scheduler_class, packets):

    scheduler = scheduler_class()
    scheduler.run(packets)

    results = calculate_metrics(
        scheduler.transmitted_packets,
        scheduler.dropped_packets,
        SIMULATION_TIME
    )

    fairness = jains_fairness(scheduler.transmitted_packets)

    return scheduler, results, fairness


# ==========================================================
# REAL-TIME QUEUE VISUALIZATION (NOW WITH PF)
# ==========================================================

def live_visualization(priority_scheduler, wfq_scheduler, pf_scheduler):

    fig, ax = plt.subplots()

    ax.set_title("Real-Time Queue Size Evolution")
    ax.set_xlabel("Time (sec)")
    ax.set_ylabel("Queue Length")

    line1, = ax.plot([], [], label="Priority")
    line2, = ax.plot([], [], label="WFQ")
    line3, = ax.plot([], [], label="PF")

    ax.legend()

    max_frames = min(
        len(priority_scheduler.time_history),
        len(wfq_scheduler.time_history),
        len(pf_scheduler.time_history)
    )

    def update(frame):

        line1.set_data(
            priority_scheduler.time_history[:frame],
            priority_scheduler.queue_history[:frame]
        )

        line2.set_data(
            wfq_scheduler.time_history[:frame],
            wfq_scheduler.queue_history[:frame]
        )

        line3.set_data(
            pf_scheduler.time_history[:frame],
            pf_scheduler.queue_history[:frame]
        )

        ax.relim()
        ax.autoscale_view()

        return line1, line2, line3

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=max_frames,
        interval=40,
        repeat=False
    )

    plt.show()


# ==========================================================
# MAIN EXECUTION
# ==========================================================

if __name__ == "__main__":

    packets = generate_traffic(SIMULATION_TIME, ARRIVAL_RATE)

    # Run all schedulers
    priority_scheduler, priority_results, priority_fairness = \
        run_scheduler(PriorityScheduler, packets.copy())

    wfq_scheduler, wfq_results, wfq_fairness = \
        run_scheduler(WFQScheduler, packets.copy())

    pf_scheduler, pf_results, pf_fairness = \
        run_scheduler(PFScheduler, packets.copy())

    print("\n========= QoS COMPARISON RESULTS =========\n")

    for traffic_type in ["voice", "video", "data"]:

        print(f"\n--- {traffic_type.upper()} ---")

        print("Priority Avg Delay:",
              round(priority_results[traffic_type]["average_delay"], 4))

        print("WFQ Avg Delay:",
              round(wfq_results[traffic_type]["average_delay"], 4))

        print("PF Avg Delay:",
              round(pf_results[traffic_type]["average_delay"], 4))

        print("Priority Loss Ratio:",
              round(priority_results[traffic_type]["loss_ratio"], 4))

        print("WFQ Loss Ratio:",
              round(wfq_results[traffic_type]["loss_ratio"], 4))

        print("PF Loss Ratio:",
              round(pf_results[traffic_type]["loss_ratio"], 4))

    print("\nOverall Throughput (Priority):",
          round(priority_results["overall_throughput"], 2), "bps")

    print("Overall Throughput (WFQ):",
          round(wfq_results["overall_throughput"], 2), "bps")

    print("Overall Throughput (PF):",
          round(pf_results["overall_throughput"], 2), "bps")

    print("\nJain's Fairness Index (Priority):",
          round(priority_fairness, 4))

    print("Jain's Fairness Index (WFQ):",
          round(wfq_fairness, 4))

    print("Jain's Fairness Index (PF):",
          round(pf_fairness, 4))

    # ======================================================
    # STATIC BAR GRAPHS (NOW 3 BARS)
    # ======================================================

    traffic_types = ["voice", "video", "data"]

    priority_delays = [priority_results[t]["average_delay"] for t in traffic_types]
    wfq_delays = [wfq_results[t]["average_delay"] for t in traffic_types]
    pf_delays = [pf_results[t]["average_delay"] for t in traffic_types]

    priority_losses = [priority_results[t]["loss_ratio"] for t in traffic_types]
    wfq_losses = [wfq_results[t]["loss_ratio"] for t in traffic_types]
    pf_losses = [pf_results[t]["loss_ratio"] for t in traffic_types]

    x = range(len(traffic_types))
    width = 0.25

    # Delay Comparison
    plt.figure()
    plt.bar([i - width for i in x], priority_delays,
            width=width, label="Priority")

    plt.bar(x, wfq_delays,
            width=width, label="WFQ")

    plt.bar([i + width for i in x], pf_delays,
            width=width, label="PF")

    plt.xticks(x, traffic_types)
    plt.title("Average Delay Comparison")
    plt.ylabel("Delay (sec)")
    plt.legend()
    plt.show()

    # Loss Comparison
    plt.figure()
    plt.bar([i - width for i in x], priority_losses,
            width=width, label="Priority")

    plt.bar(x, wfq_losses,
            width=width, label="WFQ")

    plt.bar([i + width for i in x], pf_losses,
            width=width, label="PF")

    plt.xticks(x, traffic_types)
    plt.title("Packet Loss Comparison")
    plt.ylabel("Loss Ratio")
    plt.legend()
    plt.show()

    # ======================================================
    # REAL-TIME QUEUE ANIMATION
    # ======================================================

    live_visualization(priority_scheduler, wfq_scheduler, pf_scheduler)

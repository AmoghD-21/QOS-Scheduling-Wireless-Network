import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from traffic_generator import generate_traffic
from scheduler import PriorityScheduler, WFQScheduler, PFScheduler
from metrics import calculate_metrics, jains_fairness


SIMULATION_TIME = 20


class QoSGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("QoS Scheduler Simulator")

        # -----------------------------
        # Controls Frame
        # -----------------------------
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Arrival Rate Slider
        tk.Label(control_frame, text="Arrival Rate").pack()
        self.arrival_slider = tk.Scale(
            control_frame, from_=10, to=300,
            orient=tk.HORIZONTAL
        )
        self.arrival_slider.set(120)
        self.arrival_slider.pack()

        # Buffer Size Slider
        tk.Label(control_frame, text="Buffer Size").pack()
        self.buffer_slider = tk.Scale(
            control_frame, from_=10, to=500,
            orient=tk.HORIZONTAL
        )
        self.buffer_slider.set(100)
        self.buffer_slider.pack()

        # Scheduler Selection
        tk.Label(control_frame, text="Scheduler Type").pack(pady=5)

        self.scheduler_type = tk.StringVar()
        self.scheduler_combo = ttk.Combobox(
            control_frame,
            textvariable=self.scheduler_type,
            values=["Priority", "WFQ", "PF"],
            state="readonly"
        )
        self.scheduler_combo.current(0)
        self.scheduler_combo.pack()

        # Run Button
        tk.Button(
            control_frame,
            text="Run Simulation",
            command=self.run_simulation
        ).pack(pady=10)

        # Metrics Display
        self.metrics_label = tk.Label(control_frame, text="")
        self.metrics_label.pack()

        # -----------------------------
        # Graph Frame
        # -----------------------------
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title("Queue Evolution")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Queue Size")

        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ------------------------------------------------
    # RUN SIMULATION
    # ------------------------------------------------

    def run_simulation(self):

        arrival_rate = self.arrival_slider.get()
        buffer_size = self.buffer_slider.get()
        scheduler_choice = self.scheduler_type.get()

        packets = generate_traffic(SIMULATION_TIME, arrival_rate)

        if scheduler_choice == "Priority":
            scheduler = PriorityScheduler(buffer_size)

        elif scheduler_choice == "WFQ":
            scheduler = WFQScheduler(buffer_size)

        else:
            scheduler = PFScheduler(buffer_size)

        scheduler.run(packets)

        results = calculate_metrics(
            scheduler.transmitted_packets,
            scheduler.dropped_packets,
            SIMULATION_TIME
        )

        fairness = jains_fairness(scheduler.transmitted_packets)

        # Update metrics text
        text = f"""
Throughput: {round(results['overall_throughput'], 2)} bps
Fairness: {round(fairness, 4)}
"""
        self.metrics_label.config(text=text)

        # Update Graph
        self.ax.clear()
        self.ax.plot(
            scheduler.time_history,
            scheduler.queue_history
        )
        self.ax.set_title("Queue Evolution")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Queue Size")

        self.canvas.draw()


# ------------------------------------------------
# START GUI
# ------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()
    app = QoSGUI(root)
    root.mainloop()

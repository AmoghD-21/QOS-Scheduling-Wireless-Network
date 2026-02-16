# 📡 QoS Packet Scheduling Simulator

A congestion-aware network scheduling simulator that compares **Priority Scheduling**, **Weighted Fair Queuing (WFQ)**, and **Proportional Fair (PF)** algorithms under realistic buffer and bandwidth constraints.

The simulator evaluates delay, packet loss, throughput, and fairness using Jain’s Fairness Index. It also includes an interactive GUI for real-time experimentation.

---

## 🚀 Features

- ✅ Discrete-event network simulation
- ✅ Finite buffer modeling
- ✅ Deadline-aware packet dropping
- ✅ Priority Scheduling
- ✅ Weighted Fair Queuing (WFQ) with adaptive weights
- ✅ Proportional Fair (PF) scheduling (LTE-inspired)
- ✅ Throughput, Delay & Packet Loss metrics
- ✅ Jain’s Fairness Index calculation
- ✅ Static performance comparison graphs
- ✅ Interactive GUI with real-time queue visualization

---

## 🧠 Implemented Scheduling Algorithms

### 1️⃣ Priority Scheduling
- Voice > Video > Data
- Low delay for high-priority traffic
- Risk of starvation for lower classes

### 2️⃣ Weighted Fair Queuing (WFQ)
- Assigns virtual finish time to packets
- Ensures fair bandwidth distribution
- Adaptive weight adjustment based on delay

### 3️⃣ Proportional Fair (PF)
- Selects traffic based on:
  
  metric = instantaneous_rate / average_rate

- Balances throughput and fairness
- Inspired by LTE scheduling mechanisms

---

## 📊 Performance Metrics

The simulator calculates:

- Average Delay (per traffic type)
- Packet Loss Ratio
- Overall Throughput
- Jain’s Fairness Index

---

## 🗂 Project Structure



qos_scheduler/
│
├── traffic_generator.py # Packet generation logic
├── scheduler.py # Priority, WFQ, PF implementations
├── metrics.py # Performance metric calculations
├── main.py # Static comparison + plots
├── gui_simulator.py # Interactive GUI
└── README.md


---

## ⚙️ Requirements

- Python 3.8+
- matplotlib
- tkinter (usually pre-installed)

Install dependencies:

```bash
pip install matplotlib

▶️ How To Run
🔹 Run Static Comparison (CLI Mode)
python3 main.py


This will:

Run all schedulers

Print metrics

Show comparison graphs

🔹 Run Interactive GUI
python3 gui_simulator.py


GUI Features:

Adjust Arrival Rate

Adjust Buffer Size

Select Scheduler Type

View Queue Evolution

See Throughput & Fairness instantly

📈 Example Output Metrics
VOICE Avg Delay
VIDEO Avg Delay
DATA Avg Delay

Packet Loss Ratio
Overall Throughput
Jain’s Fairness Index


Queue evolution graph shows congestion build-up and recovery cycles.

🔬 Concepts Demonstrated

Discrete Event Simulation

Queueing Theory

Congestion Modeling

Resource Allocation

Fair Scheduling

Adaptive QoS Control

LTE-inspired PF scheduling

🎓 Academic Use

This project is suitable for:

Computer Networks coursework

QoS research demonstrations

Scheduling algorithm comparison studies

Final-year academic projects

📌 Future Improvements

LTE SINR-based channel-aware PF

Multi-link simulation

CSV result export

5G NR scheduling extensions

Real-time animated GUI updates





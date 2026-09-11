# utils/plot_utils.py

import matplotlib.pyplot as plt

def plot_seir_graph(history, save_path):
    days = list(range(len(history['S'])))
    
    plt.figure(figsize=(10, 5))
    plt.plot(days, history['S'], label="Susceptible", color='green')
    plt.plot(days, history['E'], label="Exposed", color='orange')
    plt.plot(days, history['I'], label="Infected", color='red')
    plt.plot(days, history['R'], label="Recovered", color='blue')
    
    plt.title("SEIR Simulation Over Time")
    plt.xlabel("Days")
    plt.ylabel("Population Count")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()

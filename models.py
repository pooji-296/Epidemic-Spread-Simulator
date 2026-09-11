import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ✅ Epidemic Simulation Class (OOP-Based SEIR Model)
class EpidemicSimulation:
    def __init__(self, population, infected, vaccination_effect, mask, social_distancing):
        if population < 1 or infected < 1 or infected > population:
            raise ValueError("❌ Population must be at least 1, and infected must be between 1 and the population size.")

        # Store parameters
        self.population = population
        self.infected = infected
        self.vaccination_effect = vaccination_effect
        self.mask = mask
        self.social_distancing = social_distancing

        # Compute dynamic vaccination rate
        self.vaccination_rate = min(80, max(5, (infected / population) * 100)) if vaccination_effect else 0

        # SEIR Model Initialization
        self.S = [population - infected]
        self.E = [infected * 0.1]
        self.I = [infected]
        self.R = [0]

        # Transmission & recovery rates
        self.beta = 0.5 if not mask else 0.3  
        self.gamma = 0.1 if social_distancing else 0.2  

    def seasonal_effect(self, day):
        return 1 + 0.15 * np.cos(2 * np.pi * day / 365)  # Simulates seasonal transmission variations

    def run_simulation(self, days=50):
        """Runs the SEIR model simulation for a given number of days."""
        for t in range(days):
            beta_t = self.beta * self.seasonal_effect(t)
            new_exposed = beta_t * self.S[-1] * self.I[-1] / max(1, self.population)  
            new_infected = 0.2 * self.E[-1]
            new_recovered = self.gamma * self.I[-1]

            # ✅ Vaccination Effect: Reduces Susceptible Population
            vaccinated_today = (self.vaccination_rate / 100) * self.S[-1] if self.vaccination_effect else 0
            self.S.append(max(0, self.S[-1] - new_exposed - vaccinated_today))
            self.E.append(max(0, self.E[-1] + new_exposed - new_infected))
            self.I.append(max(0, self.I[-1] + new_infected - new_recovered))
            self.R.append(min(self.population, self.R[-1] + new_recovered + vaccinated_today))  

        infection_rate = round((self.I[-1] / self.population) * 100, 2)
        recovery_rate = round((self.R[-1] / self.population) * 100, 2)

        return {
            "Susceptible": self.S,
            "Exposed": self.E,
            "Infected": self.I,
            "Recovered": self.R,
            "Infection_Rate": infection_rate,
            "Recovery_Rate": recovery_rate,
            "Vaccination_Rate": self.vaccination_rate,
        }

# ✅ Graph-Based Model for Disease Spread
def graph_based_model(results, vaccination_effect):
    """Creates a network graph to visualize disease spread."""
    num_nodes = max(10, min(len(results["Susceptible"]), 500))  # Ensuring a minimum network size
    G = nx.erdos_renyi_graph(num_nodes, 0.1)  # Connectivity probability
    pos = nx.spring_layout(G)

    # Classify Nodes
    infected_nodes = np.random.choice(G.nodes, size=max(1, int(0.1 * num_nodes)), replace=False)
    recovered_nodes = np.random.choice(
        [n for n in G.nodes if n not in infected_nodes], 
        size=max(1, int(0.05 * num_nodes)), replace=False
    )
    vaccinated_nodes = []
    if vaccination_effect:
        vaccinated_nodes = np.random.choice(
            [n for n in G.nodes if n not in infected_nodes and n not in recovered_nodes], 
            size=max(1, int(0.07 * num_nodes)), replace=False
        )
    
    colors = [
        "red" if node in infected_nodes else
        "blue" if node in recovered_nodes else
        "yellow" if node in vaccinated_nodes else "green"
        for node in G.nodes
    ]

    # Plot Graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, node_color=colors, with_labels=False, node_size=50, edge_color="black")
    plt.title("📌 Epidemic Spread Graph")

    # Legend
    legend_labels = {
        "Healthy (Green)": "green",
        "Infected (Red)": "red",
        "Recovered (Blue)": "blue",
    }
    if vaccination_effect:
        legend_labels["Vaccinated (Yellow)"] = "yellow"

    for label, color in legend_labels.items():
        plt.scatter([], [], c=color, label=label)
    plt.legend()
    return plt

# ✅ Future Prediction with Epidemic Behavior (Rise, Peak, Fall)
def predict_future(results):
    """Predicts future epidemic trends with smooth rise, peak, and decline."""
    infected = results["Infected"][-1]  
    susceptible = results["Susceptible"][-1]  
    vaccination_rate = results["Vaccination_Rate"]

    if infected < 5:  
        return [infected * (1.02 ** i) for i in range(10)]  # ✅ Small values grow gradually

    # ✅ Phase 1: Controlled Growth
    R0 = 2.5  # Basic Reproduction Number
    growth_factor = 1 + (R0 - 1) * 0.2  
    peak_infected = min(susceptible * 0.6, infected * 4)  # Peak ~60% of susceptibles

    future_trend = []
    for i in range(5):  
        infected *= growth_factor * np.random.uniform(0.98, 1.02)  # Minor variation
        infected = min(infected, peak_infected)  
        future_trend.append(infected)

    # ✅ Phase 2: Peak
    future_trend.append(peak_infected)

    # ✅ Phase 3: Smooth Decline
    decline_factor = max(0.75, 1 - (vaccination_rate / 120))  
    for i in range(5):
        peak_infected *= decline_factor * np.random.uniform(0.97, 1.03)  
        future_trend.append(max(0, peak_infected))  

    return future_trend


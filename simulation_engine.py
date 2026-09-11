import numpy as np
import os
import random
import heapq
from seir.person import Person
from seir.contact_graph import ContactGraph

class SimulationEngine:
    def __init__(self, people, days=60):
        self.people = people
        self.days = days
        self.N = len(people)
        self.S_hist, self.E_hist, self.I_hist, self.R_hist = [], [], [], []
        self.daily_status = []
        self.graph = ContactGraph()
        self.priority_vaccinated_ids = set()
        self.bfs_traced_ids = []
        self._build_contact_network()

    def _build_contact_network(self):
        for i in range(self.N):
            for _ in range(3):
                j = random.randint(0, self.N - 1)
                if i != j:
                    self.graph.add_edge(self.people[i].id, self.people[j].id)

    def simulate_vaccination_priority(self, doses_per_day=10):
        queue = []
        for person in self.people:
            if person.status == 'S' and person.vaccinated == 'No':
                heapq.heappush(queue, (-person.age, person))

        for _ in range(min(doses_per_day, len(queue))):
            _, person = heapq.heappop(queue)
            person.vaccinated = 'Yes'
            person.beta = person._calculate_beta()
            self.priority_vaccinated_ids.add(person.id)

    def run(self):
        for day in range(self.days):
            new_status = [p.status for p in self.people]

            if day % 5 == 0:
                self.simulate_vaccination_priority(doses_per_day=10)

            for idx, person in enumerate(self.people):
                if person.status == 'S':
                    neighbors = self.graph.get_contacts(person.id)
                    num_infected_neighbors = sum(
                        self.people[n].status == 'I' for n in neighbors
                    )
                    if num_infected_neighbors > 0:
                        chance = 1 - np.exp(-person.beta * num_infected_neighbors / len(neighbors))
                        if np.random.rand() < chance:
                            new_status[idx] = 'E'

                elif person.status == 'E' and np.random.rand() < 0.2:
                    new_status[idx] = 'I'

                elif person.status == 'I' and np.random.rand() < 0.05:
                    new_status[idx] = 'R'

            for idx, p in enumerate(self.people):
                p.status = new_status[idx]

            self._record_day()

        return self._generate_result()

    def _record_day(self):
        self.S_hist.append(sum(p.status == 'S' for p in self.people))
        self.E_hist.append(sum(p.status == 'E' for p in self.people))
        self.I_hist.append(sum(p.status == 'I' for p in self.people))
        self.R_hist.append(sum(p.status == 'R' for p in self.people))
        self.daily_status.append([p.status for p in self.people])

    def _generate_result(self):
        r0 = np.mean([p.beta for p in self.people]) / 0.05
        peak = max(self.I_hist)
        peak_day = self.I_hist.index(peak)
        plot_filename = f"seir_plot_{os.urandom(4).hex()}.png"
        recommendation = self._generate_recommendation(r0, peak)

        infected_ids = [p.id for p in self.people if p.status == 'I']
        self.bfs_traced_ids = self.graph.trace_infection_bfs(infected_ids[0], max_depth=3) if infected_ids else []

        return {
            "history": {
                "S": self.S_hist,
                "E": self.E_hist,
                "I": self.I_hist,
                "R": self.R_hist
            },
            "r0": r0,
            "peak": peak,
            "peak_day": peak_day,
            "plot_filename": plot_filename,
            "recommendation": recommendation,
            "x": [p.x for p in self.people],
            "y": [p.y for p in self.people],
            "status": [p.status for p in self.people],
            "daily_status": self.daily_status,
            "priority_vaccinated": list(self.priority_vaccinated_ids),
            "bfs_trace": self.bfs_traced_ids
        }

    def _generate_recommendation(self, r0, peak):
        rec = []
        if r0 > 3.5:
            rec.append("🚨 Immediate lockdown advised due to high transmission (R₀ > 3.5).")
        elif r0 > 2.5:
            rec.append("⚠️ Enforce strict mask mandate and limit gatherings.")
        else:
            rec.append("🟢 Situation manageable. Maintain surveillance.")

        if peak > 0.3 * self.N:
            rec.append("📈 Over 30% population infected — prepare hospital surge capacity.")
        if any(p.age > 60 for p in self.people):
            rec.append("👴 Prioritize vaccination for seniors (60+).")
        return rec

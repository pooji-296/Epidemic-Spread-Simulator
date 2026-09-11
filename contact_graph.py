from collections import deque

class ContactGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, person_id_1, person_id_2):
        # Avoid duplicate edges and self-loops
        if person_id_1 == person_id_2:
            return
        self.graph.setdefault(person_id_1, [])
        self.graph.setdefault(person_id_2, [])
        if person_id_2 not in self.graph[person_id_1]:
            self.graph[person_id_1].append(person_id_2)
        if person_id_1 not in self.graph[person_id_2]:
            self.graph[person_id_2].append(person_id_1)

    def get_contacts(self, person_id):
        return self.graph.get(person_id, [])

    def trace_infection_bfs(self, start_id, max_depth=3):
        """Returns IDs of nodes reachable within max_depth from start_id using BFS"""
        visited = set()
        queue = deque([(start_id, 0)])
        traced = []

        while queue:
            current, depth = queue.popleft()
            if current in visited or depth > max_depth:
                continue
            visited.add(current)
            traced.append(current)
            for neighbor in self.get_contacts(current):
                queue.append((neighbor, depth + 1))
        return traced

    def get_connected_components(self):
        """Returns a list of all connected components using BFS"""
        visited = set()
        components = []

        for node in self.graph:
            if node not in visited:
                component = []
                queue = deque([node])
                while queue:
                    current = queue.popleft()
                    if current not in visited:
                        visited.add(current)
                        component.append(current)
                        queue.extend(self.get_contacts(current))
                components.append(component)

        return components

    def __repr__(self):
        edge_count = sum(len(v) for v in self.graph.values()) // 2
        return f"<ContactGraph nodes={len(self.graph)} edges={edge_count}>"

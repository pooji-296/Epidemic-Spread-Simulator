# seir/models.py

import numpy as np
from seir.person import Person
from seir.simulation_engine import SimulationEngine

def run_seir_simulation(df, days=60):
    # Ensure required columns
    if 'age' not in df or 'Masked' not in df or 'Vaccinate' not in df or 'status' not in df:
        raise ValueError("Input CSV must contain 'age', 'Masked', 'Vaccinate', 'status' columns")

    # Generate people
    people = []
    for _, row in df.iterrows():
        person = Person(
            age=int(row['age']),
            masked=row.get('Masked', 'No'),
            vaccinated=row.get('Vaccinate', 'No'),
            status=row['status'],
            x=row.get('x'),  # Optional
            y=row.get('y')   # Optional
        )
        people.append(person)

    # Run simulation
    engine = SimulationEngine(people, days=days)
    return engine.run()

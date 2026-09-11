# Epidemic Spread Simulator

## Introduction

Epidemic Spread Simulator is a Python-based application developed to simulate the spread of an infectious disease in a population. The project uses the SEIR model to represent the different stages of disease progression.

The four stages used in the simulation are Susceptible, Exposed, Infectious, and Recovered. The simulation updates the population states over a given number of days and helps in understanding how an epidemic changes over time.

The project also uses graph algorithms to represent contacts between people and perform contact tracing. A priority queue is used for vaccination prioritization.

## Objectives

The main objectives of the project are:

- To simulate disease spread using the SEIR model.
- To track the number of susceptible, exposed, infectious, and recovered people.
- To represent contacts between people using a graph.
- To perform contact tracing using Breadth First Search.
- To prioritize people for vaccination using a priority queue.
- To calculate epidemic statistics such as peak infections and R0.
- To visualize the results of the simulation.
- To provide basic recommendations based on the simulation results.

## Features

### SEIR Simulation

The simulator follows the progression:

Susceptible -> Exposed -> Infectious -> Recovered

The population in each state is recorded for every simulation day.

### Contact Graph

People in the population are represented as nodes and their interactions are represented as edges. This graph is used to study possible transmission paths.

### Contact Tracing

Breadth First Search is used to trace contacts starting from an infected person. This helps identify people who are connected through the contact network.

### Vaccination Prioritization

A priority queue is used to determine the order in which eligible people should be vaccinated. Priority can be assigned using factors such as age.

### Epidemic Analysis

The application provides information such as:

- Daily SEIR population counts
- Peak number of infections
- Day of peak infection
- Estimated R0
- Vaccination information
- Contact tracing results
- Simulation graphs

## Technologies Used

Python  
Flask  
NumPy  
Pandas  
NetworkX  
Matplotlib  
Seaborn  
SciPy  
HTML  
CSS  
JavaScript

## Project Structure

Epidemic-Spread-Simulator/

    app.py
    models.py
    requirements.txt
    README.md
    UML.png

    data/
        population_data.csv

    news_bulletin/
        news.txt

    seir/
        contact_graph.py
        models.py
        person.py
        simulation_engine.py

    static/
        css/
            styles.css
        js/
            dashboard.js

    templates/
        index.html
        dashboard.html

    utils/
        plot_utils.py

## Input

The simulator supports population data through manual input or a CSV file.

The population data can contain information such as:

- Person ID
- Age
- Initial disease status
- Mask usage
- Vaccination status

Users can also configure simulation parameters such as population size, initial infected people, simulation duration, vaccination, masking, and social distancing.

## Output

After running the simulation, the application displays the changes in the population over time. The results include the number of susceptible, exposed, infectious, and recovered people along with peak infection information and other simulation statistics.

The application also provides graphs to make the results easier to understand.

## Installation

Move into the project directory:

    cd Epidemic-Spread-Simulator

Create a virtual environment:

    python -m venv venv

Activate the environment on Windows:

    venv\Scripts\activate

Install the required packages:

    pip install -r requirements.txt

Run the application:

    python app.py

Open the local Flask address shown in the terminal to access the application.

## Working

The basic workflow of the project is:

1. Load or enter the population data.
2. Initialize the population and disease states.
3. Create the contact network.
4. Run the SEIR simulation.
5. Apply vaccination and other interventions.
6. Update the population states for each day.
7. Perform contact tracing when required.
8. Calculate epidemic statistics.
9. Display the results and graphs.

## Applications

This project can be used to understand disease transmission, epidemic behavior, contact tracing, vaccination strategies, graph algorithms, and the use of data structures in real-world problems.

It can also be extended with real-world epidemic datasets and more advanced prediction methods.

## Future Improvements

Some possible improvements include:

- Adding real-world epidemic data.
- Adding geographic-based disease spread.
- Improving contact network generation.
- Adding more vaccination strategies.
- Adding machine learning for disease prediction.
- Adding interactive network visualization.
- Adding hospital and healthcare capacity analysis.
- Supporting multiple disease variants.


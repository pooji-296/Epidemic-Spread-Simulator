<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
from seir.models import run_seir_simulation
from utils.plot_utils import plot_seir_graph
import pandas as pd
import os
import uuid

app = Flask(__name__)

DATA_PATH = "data"
STATIC_PATH = "static"
NEWS_PATH = "news_bulletin/news.txt"

@app.route('/login')
def login():
    return render_template("index.html")  # Login page

@app.route('/')
def dashboard():
    return render_template("dashboard.html")  # Main simulator page

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        uploaded_file = request.files.get('file')
        is_manual = request.form.get('manual') == 'true'

        if uploaded_file:
            file_path = os.path.join(DATA_PATH, f"uploaded_{uuid.uuid4().hex}.csv")
            uploaded_file.save(file_path)
            df = pd.read_csv(file_path)

            # Rename columns if needed
            df = df.rename(columns={
                'Age': 'age',
                'Initial_Status': 'status',
                'Masked': 'Masked',
                'Vaccinate': 'Vaccinate'
            })

            # Normalize status values
            df['status'] = df['status'].map({
                'Susceptible': 'S', 'Infectious': 'I', 'Exposed': 'E', 'Recovered': 'R'
            })

            df = df[df['status'].isin(['S', 'E', 'I', 'R'])]  # Keep valid rows only
            df = df.head(1000)  # Optional limit for performance

        elif is_manual:
            # Manual input mode
            pop_size = int(request.form.get('population', 100))
            initial_infected = int(request.form.get('initial_infected', 1))
            sim_days = int(request.form.get('days', 30))

            apply_vaccine = request.form.get('vaccination') == 'true'
            apply_mask = request.form.get('mask') == 'true'
            apply_distancing = request.form.get('distancing') == 'true'

            # Validate input
            if initial_infected > pop_size:
                return jsonify({"status": "error", "message": "Initial infected cannot exceed population size."}), 400

            # Create DataFrame with all required columns
            df = pd.DataFrame({
                'age': [20] * pop_size,
                'status': ['S'] * pop_size,
                'Masked': [apply_mask] * pop_size,
                'Vaccinate': [apply_vaccine] * pop_size
            })

            # Set initial infected individuals
            df.iloc[:initial_infected, df.columns.get_loc('status')] = 'I'

            # Optional: store distancing flag
            df.attrs['distancing'] = apply_distancing

        else:
            return jsonify({"status": "error", "message": "No input provided."}), 400

        # Run SEIR simulation
        result = run_seir_simulation(df)

        # Plot results
        plot_path = os.path.join(STATIC_PATH, result["plot_filename"])
        plot_seir_graph(result["history"], plot_path)

        # Bulletin text
        bulletin_text = (
            f"🦠 Simulation Completed\n"
            f"📈 Peak Infections: {result['peak']} on Day {result['peak_day']}\n"
            f"🔬 Estimated R₀: {result['r0']:.2f}\n"
        )
        with open(NEWS_PATH, "w", encoding="utf-8") as f:
            f.write(bulletin_text)

        # Return simulation results to frontend
        return jsonify({
            "status": "success",
            "peak": int(result["peak"]),
            "peak_day": int(result["peak_day"]),
            "r0": float(result["r0"]),
            "history": {
                "S": list(map(int, result["history"]["S"])),
                "E": list(map(int, result["history"]["E"])),
                "I": list(map(int, result["history"]["I"])),
                "R": list(map(int, result["history"]["R"]))
            },
            "bulletin": bulletin_text,
            "recommendation": result.get("recommendation", []),
            "x": result["x"],
            "y": result["y"],
            "daily_status": result["daily_status"],
            "priority_vaccinated": result.get("priority_vaccinated", []),
            "bfs_trace": result.get("bfs_trace", [])
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    os.makedirs(DATA_PATH, exist_ok=True)
    os.makedirs(STATIC_PATH, exist_ok=True)
    os.makedirs("news_bulletin", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    app.run(debug=True)
=======
from flask import Flask, render_template, request, jsonify
from seir.models import run_seir_simulation
from utils.plot_utils import plot_seir_graph
import pandas as pd
import os
import uuid

app = Flask(__name__)

DATA_PATH = "data"
STATIC_PATH = "static"
NEWS_PATH = "news_bulletin/news.txt"

@app.route('/login')
def login():
    return render_template("index.html")  # Login page

@app.route('/')
def dashboard():
    return render_template("dashboard.html")  # Main simulator page

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        uploaded_file = request.files.get('file')
        is_manual = request.form.get('manual') == 'true'

        if uploaded_file:
            file_path = os.path.join(DATA_PATH, f"uploaded_{uuid.uuid4().hex}.csv")
            uploaded_file.save(file_path)
            df = pd.read_csv(file_path)

            # Rename columns if needed
            df = df.rename(columns={
                'Age': 'age',
                'Initial_Status': 'status',
                'Masked': 'Masked',
                'Vaccinate': 'Vaccinate'
            })

            # Normalize status values
            df['status'] = df['status'].map({
                'Susceptible': 'S', 'Infectious': 'I', 'Exposed': 'E', 'Recovered': 'R'
            })

            df = df[df['status'].isin(['S', 'E', 'I', 'R'])]  # Keep valid rows only
            df = df.head(1000)  # Optional limit for performance

        elif is_manual:
            # Manual input mode
            pop_size = int(request.form.get('population', 100))
            initial_infected = int(request.form.get('initial_infected', 1))
            sim_days = int(request.form.get('days', 30))

            apply_vaccine = request.form.get('vaccination') == 'true'
            apply_mask = request.form.get('mask') == 'true'
            apply_distancing = request.form.get('distancing') == 'true'

            # Validate input
            if initial_infected > pop_size:
                return jsonify({"status": "error", "message": "Initial infected cannot exceed population size."}), 400

            # Create DataFrame with all required columns
            df = pd.DataFrame({
                'age': [20] * pop_size,
                'status': ['S'] * pop_size,
                'Masked': [apply_mask] * pop_size,
                'Vaccinate': [apply_vaccine] * pop_size
            })

            # Set initial infected individuals
            df.iloc[:initial_infected, df.columns.get_loc('status')] = 'I'

            # Optional: store distancing flag
            df.attrs['distancing'] = apply_distancing

        else:
            return jsonify({"status": "error", "message": "No input provided."}), 400

        # Run SEIR simulation
        result = run_seir_simulation(df)

        # Plot results
        plot_path = os.path.join(STATIC_PATH, result["plot_filename"])
        plot_seir_graph(result["history"], plot_path)

        # Bulletin text
        bulletin_text = (
            f"🦠 Simulation Completed\n"
            f"📈 Peak Infections: {result['peak']} on Day {result['peak_day']}\n"
            f"🔬 Estimated R₀: {result['r0']:.2f}\n"
        )
        with open(NEWS_PATH, "w", encoding="utf-8") as f:
            f.write(bulletin_text)

        # Return simulation results to frontend
        return jsonify({
            "status": "success",
            "peak": int(result["peak"]),
            "peak_day": int(result["peak_day"]),
            "r0": float(result["r0"]),
            "history": {
                "S": list(map(int, result["history"]["S"])),
                "E": list(map(int, result["history"]["E"])),
                "I": list(map(int, result["history"]["I"])),
                "R": list(map(int, result["history"]["R"]))
            },
            "bulletin": bulletin_text,
            "recommendation": result.get("recommendation", []),
            "x": result["x"],
            "y": result["y"],
            "daily_status": result["daily_status"],
            "priority_vaccinated": result.get("priority_vaccinated", []),
            "bfs_trace": result.get("bfs_trace", [])
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    os.makedirs(DATA_PATH, exist_ok=True)
    os.makedirs(STATIC_PATH, exist_ok=True)
    os.makedirs("news_bulletin", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    app.run(debug=True)
>>>>>>> 19cda4e088f914d8f6d880543348d2eaef6c4eae

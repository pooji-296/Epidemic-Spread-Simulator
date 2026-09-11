import pandas as pd

def load_data(file):
    """Loads dataset from user upload with validation, type conversion, and error handling."""
    try:
        df = pd.read_csv(file)

        # Ensure dataset is not empty
        if df.empty:
            raise ValueError("Uploaded dataset is empty. Please provide valid data.")

        # Convert 'Yes/No' or 'True/False' columns to 0/1 for better processing
        for col in ["Mask_Mandate", "Social_Distancing"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower().map({"yes": 1, "no": 0, "true": 1, "false": 0}).fillna(0).astype(int)

        # Ensure required columns exist
        required_columns = ["Population", "Initial_Infected", "Mask_Mandate", "Social_Distancing"]
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Dataset is missing required columns: {', '.join(missing_cols)}")

        # Handle missing values by filling with reasonable defaults
        df.fillna({
            "Population": df["Population"].median() if "Population" in df else 10000,
            "Initial_Infected": df["Initial_Infected"].median() if "Initial_Infected" in df else 10
        }, inplace=True)

        # Convert numeric columns to integer
        for col in ["Population", "Initial_Infected"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        return df

    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None  # Return None so Streamlit can handle the error

import pandas as pd
import traceback
import matplotlib.pyplot as plt
import seaborn as sns
import io
import traceback
from PIL import Image
import os

from rules import (
    validate_identifier_type, validate_accounting_intent, validate_type_of_hedge,
    validate_hedged_risk, validate_hedge_interest_rate, validate_hedge_percentage,
    validate_hedge_horizon, validate_hedged_cash_flow, validate_sidedness,
    validate_hedging_instrument_at_fair_value
)


# Define the results directory
RESULTS_DIR = "results"

# Ensure the directory exists
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)  # Create directory if it doesn't exist

# -------------------------------------- CSV Validation --------------------------------------

def validate_csv(csv_file):
    """Validate CSV and return results with full error handling"""
    try:
        if csv_file is None:
            return "❌ No CSV file uploaded.", None, None

        try:
            df = pd.read_csv(csv_file, encoding="utf-8")  # Try UTF-8 encoding
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, encoding="ISO-8859-1")  # Fallback encoding
        except Exception as e:
            return f"❌ Error reading CSV:\n{traceback.format_exc()}", None, None

        # Define column weights (sum = 1)
        WEIGHTS = {
            "Identifier Type": 0.05, "Identifier Value": 0.05,
            "Amortized Cost (USD Equivalent)": 0.10, "Market Value (USD Equivalent)": 0.10,
            "Accounting Intent (AFS, HTM, EQ)": 0.08, "Type of Hedge(s)": 0.07,
            "Hedged Risk": 0.08, "Hedge Interest Rate": 0.07, "Hedge Percentage": 0.10,
            "Hedge Horizon": 0.08, "Hedged Cash Flow": 0.07, "Sidedness": 0.05,
            "Hedging Instrument at Fair Value": 0.10,
        }

        # Mapping validation functions
        VALIDATION_FUNCTIONS = {
            "Identifier Type": validate_identifier_type, "Accounting Intent (AFS, HTM, EQ)": validate_accounting_intent,
            "Type of Hedge(s)": validate_type_of_hedge, "Hedged Risk": validate_hedged_risk,
            "Hedge Interest Rate": validate_hedge_interest_rate, "Hedge Percentage": validate_hedge_percentage,
            "Hedge Horizon": validate_hedge_horizon, "Hedged Cash Flow": validate_hedged_cash_flow,
            "Sidedness": validate_sidedness, "Hedging Instrument at Fair Value": validate_hedging_instrument_at_fair_value,
        }

        # Calculate anomaly score
        def calculate_anomaly_score(row):
            total_weight = 0
            for column, weight in WEIGHTS.items():
                if column in VALIDATION_FUNCTIONS:
                    validation_func = VALIDATION_FUNCTIONS[column]
                    try:
                        if not validation_func(pd.DataFrame([row]))[column].empty:
                            total_weight += weight
                    except Exception as e:
                        return f"❌ Validation error in '{column}': {traceback.format_exc()}"
            return total_weight

        # Apply validation
        df["Anomaly Score"] = df.apply(calculate_anomaly_score, axis=1)
        df["Is Anomalous"] = df["Anomaly Score"] > 0.5

        # Save validated CSV
        validated_csv_path = os.path.join(RESULTS_DIR, "validated_results.csv")
        df.to_csv(validated_csv_path, index=False)

        return df, "✅ CSV validation successful.", validated_csv_path
    except Exception as e:
        return f"❌ Unexpected error in validation:\n{traceback.format_exc()}", None, None


# -------------------------------------- Scatter Plot --------------------------------------
def plot_anomalies(df):
    """Generate scatter plot for anomalies and return image."""
    try:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=df.index, y=df["Anomaly Score"], hue=df["Is Anomalous"],
                        palette={True: "red", False: "blue"}, alpha=0.6)
        plt.axhline(y=0.5, color='gray', linestyle='--', label="Anomaly Threshold (0.5)")
        plt.xlabel("Row Index")
        plt.ylabel("Anomaly Score")
        plt.title("Anomalies Detection Scatter Plot")
        plt.legend(title="Anomalous", labels=["Normal (Blue)", "Anomalous (Red)"])

        # Convert plot to image
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        plt.close()
        img_buffer.seek(0)
        return Image.open(img_buffer)
    except Exception:
        return f"❌ Error generating plot:\n{traceback.format_exc()}"

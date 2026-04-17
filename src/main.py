from data_loader import load_data
from preprocessing import preprocess_data
from feature_engineering import extract_features
from model_training import train_model
import pandas as pd

def run_pipeline():
    print("🚀 Starting HAR Pipeline...\n")

    # Step 1: Load data
    df = load_data("../data/raw_data.csv")

    if df is None:
        return

    # Step 2: Preprocess
    X_scaled, y, scaler = preprocess_data(df)

    # Step 3: Feature Engineering
    X_features = extract_features(X_scaled)

    # Step 4: Train Model
    model = train_model(X_features, y)

    # Step 5: Save processed data (for your app.py)
    final_df = pd.DataFrame(X_features, columns=["mean", "std", "max", "min"])
    final_df["Activity"] = y.values

    final_df.to_csv("../output/final_data.csv", index=False)

    print("\n✅ Pipeline completed successfully")
    print("📁 Output saved to: output/final_data.csv")

if __name__ == "__main__":
    run_pipeline()
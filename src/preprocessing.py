from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    # Drop missing values
    df = df.dropna()

    # Separate features and label
    if "Activity" not in df.columns:
        raise ValueError("❌ 'Activity' column not found in dataset")

    X = df.drop("Activity", axis=1)
    y = df["Activity"]

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("✅ Preprocessing complete")
    return X_scaled, y, scaler
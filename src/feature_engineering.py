import numpy as np

def extract_features(X):
    features = []

    for row in X:
        mean = np.mean(row)
        std = np.std(row)
        max_val = np.max(row)
        min_val = np.min(row)

        features.append([mean, std, max_val, min_val])

    print("✅ Features extracted")
    return np.array(features)
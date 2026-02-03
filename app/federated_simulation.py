# Federated Learning Simulation for EHR Blockchain Project
# This script is safe and does not affect your main app.
# It simulates multiple hospitals training local models and sharing hashes on the blockchain.

import os
import random
import hashlib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from app.services.blockchain_service import BlockchainService

# Simulate 3 hospitals with their own data
def generate_hospital_data(n_samples=100, n_features=5, random_state=None):
    X, y = make_classification(n_samples=n_samples, n_features=n_features, n_informative=3, n_redundant=0, random_state=random_state)
    return X, y

# Simulate local training and return model weights
def train_local_model(X, y):
    model = LogisticRegression(max_iter=100)
    model.fit(X, y)
    return model.coef_.flatten(), model.intercept_.flatten()

# Hash model weights for blockchain storage
def hash_model(weights):
    w_bytes = np.array(weights).tobytes()
    return hashlib.sha256(w_bytes).hexdigest()

# Simulate federated learning round
def federated_round(hospitals, blockchain_service):
    local_hashes = []
    local_weights = []
    print("\n--- Federated Learning Round ---")
    for i, (X, y) in enumerate(hospitals):
        weights, intercept = train_local_model(X, y)
        all_weights = np.concatenate([weights, intercept])
        model_hash = hash_model(all_weights)
        print(f"Hospital {i+1} model hash: {model_hash}")
        # Store hash on blockchain (simulate)
        # blockchain_service.store_model_hash(model_hash)  # Uncomment if you add this method
        local_hashes.append(model_hash)
        local_weights.append(all_weights)
    # Aggregate (average) weights
    global_weights = np.mean(local_weights, axis=0)
    global_hash = hash_model(global_weights)
    print(f"Global model hash: {global_hash}")
    # blockchain_service.store_model_hash(global_hash)  # Uncomment if you add this method
    return local_hashes, global_hash

if __name__ == "__main__":
    # Setup blockchain service (read-only, safe)
    blockchain_service = BlockchainService()
    blockchain_service.connect_to_ganache()
    # Generate data for 3 hospitals
    hospitals = [generate_hospital_data(random_state=i) for i in range(3)]
    # Run a federated learning round
    local_hashes, global_hash = federated_round(hospitals, blockchain_service)
    print("\nSimulation complete. (Hashes not stored on blockchain unless you add that method)")

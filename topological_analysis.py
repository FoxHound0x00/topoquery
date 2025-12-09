"""
Apply topological analysis using the hole library
"""
import sys
import os

# Add HOLE library to path (adjust if needed)
hole_path = os.environ.get('HOLE_PATH', '../hole')
if os.path.exists(hole_path):
    sys.path.insert(0, hole_path)

import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from hole.core.distance_metrics import distance_matrix

def compute_distance_matrices():
    """Compute distance matrices using multiple metrics"""
    print("Computing topological features...")
    
    # Load parsed features
    with open('queries/parsed_features.json', 'r') as f:
        data = json.load(f)
    
    feature_matrix = np.array(data['feature_matrix'])
    
    # Normalize features
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(feature_matrix)
    
    print(f"✓ Feature matrix shape: {normalized_features.shape}")
    
    # Compute multiple distance metrics
    metrics = ['euclidean', 'cosine', 'mahalanobis']
    distance_matrices = {}
    
    for metric in metrics:
        print(f"  - Computing {metric} distance...")
        try:
            dist_mat = distance_matrix(normalized_features, metric=metric)
            distance_matrices[metric] = dist_mat.tolist()
        except Exception as e:
            print(f"    Warning: {metric} failed ({e}), skipping")
    
    # Save results
    output = {
        'normalized_features': normalized_features.tolist(),
        'distance_matrices': distance_matrices,
        'metrics': list(distance_matrices.keys())
    }
    
    with open('outputs/topological_features.json', 'w') as f:
        json.dump(output, f)
    
    print(f"✓ Computed {len(distance_matrices)} distance matrices")
    print(f"✓ Metrics: {list(distance_matrices.keys())}")
    print(f"✓ Saved to: outputs/topological_features.json")
    print()

if __name__ == '__main__':
    compute_distance_matrices()


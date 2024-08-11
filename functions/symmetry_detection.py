# symmetry_detection.py
import numpy as np

def detect_symmetry(points):
    # Reflect points over their centroid
    centroid = np.mean(points, axis=0)
    reflected_points = 2 * centroid - points
    
    # Check for symmetry by comparing original and reflected points
    differences = np.linalg.norm(points - reflected_points, axis=1)
    symmetry = np.all(differences < 1e-6)  # Tolerance for floating point comparison
    
    return symmetry

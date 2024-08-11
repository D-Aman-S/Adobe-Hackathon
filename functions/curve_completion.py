# curve_completion.py
import numpy as np
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression

def complete_curve(points, occlusion_type='connected'):
    if occlusion_type == 'connected':
        # Use interpolation to complete the curve
        x = points[:, 0]
        y = points[:, 1]
        f = interp1d(x, y, kind='linear')
        new_x = np.linspace(x[0], x[-1], num=500)
        new_y = f(new_x)
        completed_points = np.column_stack((new_x, new_y))
        return completed_points
    elif occlusion_type == 'disconnected':
        # Handle disconnected occlusions by connecting endpoints
        completed_points = handle_disconnected_occlusions(points)
        return completed_points

def handle_disconnected_occlusions(points):
    """
    Handle disconnected occlusions by connecting the endpoints of fragments.
    """
    if len(points) < 2:
        return points
    
    # Find start and end points
    start_point = points[0]
    end_point = points[-1]
    
    # Create a line connecting the start and end points
    lin_reg = LinearRegression()
    lin_reg.fit(points[:, 0].reshape(-1, 1), points[:, 1])
    new_x = np.linspace(start_point[0], end_point[0], num=500)
    new_y = lin_reg.predict(new_x.reshape(-1, 1))
    
    # Concatenate original points with the new points
    completed_points = np.vstack((points, np.column_stack((new_x, new_y))))
    return completed_points

# Example usage in __1.py
if __name__ == "__main__":
    import sys
    from utils import read_csv, plot, polylines2svg
    from regularization import fit_line, fit_circle
    from symmetry_detection import detect_symmetry
    from curve_completion import complete_curve

    input_path = 'problems/problems/isolated.csv'
    output_svg_path = 'problems/problems/output.svg'
    
    paths_XYs = read_csv(input_path)
    for path in paths_XYs:
        for points in path:
            m, c = fit_line(points)
            print(f'Line fit: y = {m}x + {c}')
            
            xc, yc, R = fit_circle(points)
            print(f'Circle fit: center=({xc}, {yc}), radius={R}')
            
            symmetry = detect_symmetry(points)
            print(f'Symmetry detected: {symmetry}')
            
            completed_points = complete_curve(points, occlusion_type='connected')
            print(f'Completed curve points: {completed_points}')
            
            plot(paths_XYs)
            polylines2svg(paths_XYs, output_svg_path)

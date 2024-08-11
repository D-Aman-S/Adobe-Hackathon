# __1__.py
import os
from utils import read_csv, plot, polylines2svg
from regularization import fit_line, fit_circle
from symmetry_detection import detect_symmetry
from curve_completion import complete_curve

def process_file(input_path, output_svg_path):
    # Read CSV file
    paths_XYs = read_csv(input_path)
    
    # Process each path
    for path in paths_XYs:
        for points in path:
            # Fit line
            m, c = fit_line(points)
            print(f'Line fit: y = {m}x + {c}')
            
            # Fit circle
            xc, yc, R = fit_circle(points)
            print(f'Circle fit: center=({xc}, {yc}), radius={R}')
            
            # Detect symmetry
            symmetry = detect_symmetry(points)
            print(f'Symmetry detected: {symmetry}')
            
            # Complete curve
            completed_points = complete_curve(points, occlusion_type='connected')
            print(f'Completed curve points: {completed_points}')
            
    # Visualize the results
    plot(paths_XYs)
    
    # Save the output as SVG
    polylines2svg(paths_XYs, output_svg_path)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(current_dir, 'problems')
    output_directory = os.path.join(current_dir, 'problems', 'output')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # List of input files
    input_files = [
        'isolated.csv',
        'frag0.csv',
        'frag1.csv',
        'frag2.csv',
        'occlusion1.csv',
        # Add other files as needed
    ]
    
    # Process each file
    for input_file in input_files:
        input_path = os.path.join(input_directory, input_file)
        output_svg_path = os.path.join(output_directory, input_file.replace('.csv', '.svg'))
        print(f'Processing {input_file}...')
        process_file(input_path, output_svg_path)
        print(f'Saved output to {output_svg_path}')

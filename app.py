from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os
from functions.utils import read_csv, read_svg, polylines2svg, plot
from functions.regularization import fit_line, fit_circle
from functions.symmetry_detection import detect_symmetry
from functions.curve_completion import complete_curve

app = Flask(__name__)
UPLOAD_DIRECTORY = 'uploaded_files'
OUTPUT_DIRECTORY = 'output_files'
PERMITTED_EXTENSIONS = {'csv', 'svg'}

app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY
app.config['OUTPUT_DIRECTORY'] = OUTPUT_DIRECTORY

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

def is_file_allowed(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in PERMITTED_EXTENSIONS

def handle_file_processing(input_file_path, output_svg_file_path):
    if input_file_path.lower().endswith('.csv'):
        path_coordinates = read_csv(input_file_path)
    elif input_file_path.lower().endswith('.svg'):
        path_coordinates = read_svg(input_file_path)
    else:
        raise ValueError("File type not supported")

    for path in path_coordinates:
        for points in path:
            slope, intercept = fit_line(points)
            print(f'Fitted line: y = {slope}x + {intercept}')
            center_x, center_y, radius = fit_circle(points)
            print(f'Fitted circle: center=({center_x}, {center_y}), radius={radius}')
            symmetry = detect_symmetry(points)
            print(f'Detected symmetry: {symmetry}')
            completed_curve = complete_curve(points, occlusion_type='connected')
            print(f'Completed curve points: {completed_curve}')
    
    svg_plot_path = os.path.join(app.config['OUTPUT_DIRECTORY'], 'plot.svg')
    png_plot_path = os.path.join(app.config['OUTPUT_DIRECTORY'], 'plot.png')

    plot(path_coordinates, svg_plot_path, png_plot_path)
    polylines2svg(path_coordinates, output_svg_file_path)
    
    return output_svg_file_path, svg_plot_path, png_plot_path

@app.route('/')
def display_upload_form():
    return render_template('homepage.html')

@app.route('/', methods=['POST'])
def process_uploaded_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    uploaded_file = request.files['file']
    
    if uploaded_file.filename == '':
        return redirect(request.url)
    
    if uploaded_file and is_file_allowed(uploaded_file.filename):
        safe_filename = secure_filename(uploaded_file.filename)
        input_file_path = os.path.join(app.config['UPLOAD_DIRECTORY'], safe_filename)
        uploaded_file.save(input_file_path)
        
        output_svg_file_path = os.path.join(app.config['OUTPUT_DIRECTORY'], safe_filename.rsplit('.', 1)[0] + '.svg')
        
        output_svg_file_path, svg_plot_path, png_plot_path = handle_file_processing(input_file_path, output_svg_file_path)
        
        return render_template('homepage.html', 
                               svg_file=url_for('serve_uploaded_file', filename=safe_filename.rsplit('.', 1)[0] + '.svg'),
                               plot_svg_file=url_for('serve_uploaded_plot', ext='svg'),
                               plot_png_file=url_for('serve_uploaded_plot', ext='png'))
    return redirect(request.url)

@app.route('/uploaded_files/plot.<ext>')
def serve_uploaded_plot(ext):
    if ext not in ['svg', 'png']:
        return "File not found", 404
    return send_from_directory(app.config['OUTPUT_DIRECTORY'], f'plot.{ext}')

@app.route('/uploaded_files/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['OUTPUT_DIRECTORY'], filename)

if __name__ == "__main__":
    app.run(debug=True)

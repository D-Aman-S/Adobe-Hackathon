import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from svgpathtools import parse_path

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def read_svg(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    
    paths = []
    for path_elem in root.findall('.//svg:path', namespaces):
        d = path_elem.attrib.get('d', '')
        points = parse_svg_path(d)
        if points.size > 0:
            paths.append([points])
    return paths

def parse_svg_path(d):
    path = parse_path(d)
    points = []
    for segment in path:
        for point in segment:
            points.append([point.real, point.imag])
    return np.array(points)

def plot(paths_XYs, output_svg_path, output_png_path):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(paths_XYs):
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], linewidth=2)
    ax.set_aspect('equal')
    
    # Save as SVG
    plt.savefig(output_svg_path, format='svg')  # Save as SVG
    # Save as PNG
    plt.savefig(output_png_path, format='png')  # Save as PNG
    plt.close()  # Close the plot to free up memory

def polylines2svg(paths_XYs, svg_path):
    import svgwrite
    import cairosvg
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)
    
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    for i, path in enumerate(paths_XYs):
        path_data = []
        for XY in path:
            path_data.append(("M", (XY[0, 0], XY[0, 1])))
            for j in range(1, len(XY)):
                path_data.append(("L", (XY[j, 0], XY[j, 1])))
            if not np.allclose(XY[0], XY[-1]):
                path_data.append(("Z", None))
        group.add(dwg.path(d=path_data, fill='none', stroke='black', stroke_width=2))
    dwg.add(group)
    dwg.save()
    
    png_path = svg_path.replace('.svg', '.png')
    fact = max(1, 1024 // min(H, W))
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=W, parent_height=H,
                     output_width=fact * W, output_height=fact * H, background_color='white')

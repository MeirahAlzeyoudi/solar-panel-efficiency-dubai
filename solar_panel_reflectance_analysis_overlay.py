import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import rasterio
from shapely.geometry import Polygon, Point

# You must set these paths appropriately before running the script
workspace = "path_to_your_images_folder"
output_path = os.path.join(workspace, "Performance_Analysis")
os.makedirs(output_path, exist_ok=True)

def calculate_ndvi(red_band, nir_band):
    ndvi = (nir_band - red_band) / (np.maximum(nir_band + red_band, 1e-10))
    return np.clip(ndvi, -1.0, 1.0)

def calculate_ndri(red_band, nir_band):
    ndri = (nir_band - red_band) / (np.maximum(nir_band + red_band, 1e-10))
    return np.clip(ndri, -1.0, 1.0)

def map_reflectance_to_color(reflectance_array, is_ndvi=True):
    color_map = np.zeros((reflectance_array.shape[0], reflectance_array.shape[1], 4), dtype=np.uint8)
    color_ranges = [
        ((-1.0, -0.75), (255, 0, 0, 255)),
        ((-0.75, -0.5), (255, 165, 0, 255)),
        ((-0.5, -0.25), (255, 255, 0, 255)),
        ((-0.25, 0.0), (173, 255, 47, 255)),
        ((0.0, 0.25), (144, 238, 144, 255)),
        ((0.25, 0.5), (0, 255, 0, 255)),
        ((0.5, 0.75), (0, 128, 0, 255)),
        ((0.75, 1.0), (0, 50, 0, 255)),
    ]
    for value_range, color in color_ranges:
        mask = (reflectance_array >= value_range[0]) & (reflectance_array < value_range[1])
        color_map[mask] = color
    return color_map

def detect_desert_region(true_color_img, threshold=(200, 200, 150)):
    desert_mask = np.zeros(true_color_img.shape[:2], dtype=bool)
    for row in range(true_color_img.shape[0]):
        for col in range(true_color_img.shape[1]):
            r, g, b = true_color_img[row, col]
            if r > threshold[0] and g > threshold[1] and b < threshold[2]:
                desert_mask[row, col] = True
    return desert_mask

def apply_polygon_mask(reflectance_array, polygon_coords, color_map, transform):
    height, width = reflectance_array.shape
    overlay = np.zeros((height, width, 4), dtype=np.uint8)
    polygon = Polygon([(int((lon - transform[2]) / transform[0]), 
                        int((lat - transform[5]) / transform[4])) 
                       for lon, lat in polygon_coords])
    for row in range(height):
        for col in range(width):
            point = Point(col, row)
            if polygon.contains(point):
                overlay[row, col] = color_map[row, col]
            else:
                overlay[row, col] = [0, 0, 0, 0]
    return overlay

def create_reflectance_overlay(reflectance_array, true_color_path, date, output_path, polygon_coords, transform, reflectance_type="NDVI"):
    true_color_img = plt.imread(true_color_path)
    height, width = reflectance_array.shape
    desert_mask = detect_desert_region(true_color_img)
    color_map = map_reflectance_to_color(reflectance_array, is_ndvi=(reflectance_type == "NDVI"))
    color_map[desert_mask] = [0, 0, 0, 0]
    overlay_img = apply_polygon_mask(reflectance_array, polygon_coords, color_map, transform)

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(true_color_img, extent=[0, width, 0, height])
    ax.imshow(overlay_img, extent=[0, width, 0, height], alpha=0.6)
    plt.title(f'{reflectance_type} Analysis Overlay - {date}', fontsize=16)
    plt.axis('off')

    legend_elements = [
        Patch(facecolor=(255/255, 0, 0), edgecolor='k', label='Very Low Efficiency'),
        Patch(facecolor=(255/255, 165/255, 0), edgecolor='k', label='Low Efficiency'),
        Patch(facecolor=(1, 1, 0), edgecolor='k', label='Moderate Efficiency'),
        Patch(facecolor=(173/255, 1, 47/255), edgecolor='k', label='High Efficiency'),
        Patch(facecolor=(144/255, 238/255, 144/255), edgecolor='k', label='Very High Efficiency'),
        Patch(facecolor=(0, 1, 0), edgecolor='k', label='Higher Efficiency'),
        Patch(facecolor=(0, 128/255, 0), edgecolor='k', label='Optimal Performance'),
        Patch(facecolor=(0, 50/255, 0), edgecolor='k', label='Maximum Performance'),
    ]
    plt.legend(handles=legend_elements, loc='upper center', fontsize=10, bbox_to_anchor=(0.5, -0.15),
               title="Performance Levels", ncol=4)
    output_filename = os.path.join(output_path, f"{reflectance_type}_Overlay_{date}.png")
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()

def group_images_by_date(workspace):
    image_dict = {}
    for img_path in glob.glob(os.path.join(workspace, "*.tiff")):
        date = os.path.basename(img_path)[:10]
        if date not in image_dict:
            image_dict[date] = {'True_Color': None, 'B04': None, 'B08': None}
        if "True_color" in img_path:
            image_dict[date]['True_Color'] = img_path
        elif "B04" in img_path:
            image_dict[date]['B04'] = img_path
        elif "B08" in img_path:
            image_dict[date]['B08'] = img_path
    return image_dict

# Example polygon coordinates (long, lat)
polygon_coordinates = [(54.5, 24.3), (54.6, 24.3), (54.6, 24.4), (54.5, 24.4)]

# Process grouped image data
image_dict = group_images_by_date(workspace)
for date, images in image_dict.items():
    if images['True_Color'] and images['B04'] and images['B08']:
        with rasterio.open(images['B04']) as red_file, rasterio.open(images['B08']) as nir_file:
            red_band = red_file.read(1)
            nir_band = nir_file.read(1)
            transform = red_file.transform
            ndvi = calculate_ndvi(red_band, nir_band)
            ndri = calculate_ndri(red_band, nir_band)
            create_reflectance_overlay(ndvi, images['True_Color'], date, output_path, polygon_coordinates, transform, reflectance_type="NDVI")
            create_reflectance_overlay(ndri, images['True_Color'], date, output_path, polygon_coordinates, transform, reflectance_type="NDRI")

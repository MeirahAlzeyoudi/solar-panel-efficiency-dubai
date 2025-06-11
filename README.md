# Solar Panel Detection and Performance Monitoring Using Deep Learning

## Project Description

Solar power is a clean, renewable energy source. To meet growing energy demands and replace conventional power sources, countries are scaling up solar photovoltaic (PV) parks. Some of these parks span thousands of acres and house millions of solar panels.

Traditional methods for monitoring these facilities—like surveys and manual inspections—are time-consuming and often inaccurate. This project uses deep learning with satellite imagery to automate the detection and performance evaluation of solar panel fields, helping governments, researchers, and energy companies identify working vs. underperforming infrastructure.

---

## Objective

- Automatically detect and classify solar photovoltaic parks using Sentinel-2 imagery  
- Monitor thermal anomalies that may indicate damaged or non-functioning solar panels  
- Provide visual insights for maintenance planning and policy decisions  

---

## Tools Used

- **QGIS** – for spatial visualization and post-processing  
- **ArcGIS Pro (Deep Learning Toolbox)** – for model training and classification  
- **Python (ArcGIS Python window)** – for automation and preprocessing  
- **Sentinel-2 L2A imagery** – satellite source (12 bands, 10m resolution)

---

## Deep Learning Model

- **Model:** UNet architecture for pixel classification  
- **Source:** [Solar Photovoltaic Park Classifier (ArcGIS Model)](https://www.arcgis.com/home/item.html?id=55600a3a452c4b208d3c54026c3f7cd1)  
- **Accuracy:** 99% overall accuracy  
  - Precision: 0.966  
  - Recall: 0.967  
  - F1 Score: 0.967  
- **Training Data:** Esri proprietary dataset, further enhanced using local samples  
- **Limitations:** Some false positives near mountains, coastal zones, or cloudy areas  

---

## Methodology

### 1. Data Collection
- Downloaded high-resolution Sentinel-2 L2A imagery over Dubai’s solar panel farms.
- Used ArcGIS and QGIS to preview, filter, and prepare the raster scenes.

### 2. Training Samples
- Generated labeled training samples manually in ArcGIS Pro based on known solar farm boundaries.

### 3. Model Training
- Used the **Train Deep Learning Model** tool in ArcGIS Pro to fine-tune the UNet classifier.
- Conducted training with multi-band raster input and masked feature layers.

### 4. Classification
- Applied the **Classify Pixels Using Deep Learning** tool to detect solar panels in new imagery.

### 5. Thermal Anomaly Detection
- Analyzed thermal bands and spectral indices (e.g., Band 4, Band 8, and Band 10).
- Detected temperature “scapes” indicating malfunctioning or low-efficiency solar panels.

### 6. Output & Visualization
- Generated classified rasters showing PV park locations and temperature anomalies.
- Exported final results as high-resolution images and layered map files.

---

## Output Folders
- `/images/` – Final visualizations of solar detection and thermal performance  


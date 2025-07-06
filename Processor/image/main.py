# views.py
from django.shortcuts import render
from .form import LocationForm
from .models import NDVIPlot, Water
import ee  # Earth Engine API
import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
import requests
import zipfile
from io import BytesIO
from django.core.files.base import ContentFile
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
# Authenticate and initialize Earth Engine
ee.Authenticate()
project_id = 'ee-yashvchavan07'
ee.Initialize(project=project_id)

def index(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            # Get user input for latitude and longitude
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']

            try:
                # Define a small rectangular region (~10x10 km)
                geometry = ee.Geometry.Rectangle(
                    [longitude - 0.05, latitude - 0.05, 
                     longitude + 0.05, latitude + 0.05]
                )

                # Load Sentinel-2 image with minimal cloud cover
                sentinel2 = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
                    .filterBounds(geometry) \
                    .filterDate('2022-01-01', '2022-12-31') \
                    .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 1) \
                    .median().clip(geometry)

                # Select RGB + NIR bands and apply scaling factor
                bands = ['B4', 'B3', 'B2', 'B8']  # Red, Green, Blue, NIR
                image = sentinel2.select(bands).multiply(0.0001)

                # Get download URL
                url = image.getDownloadURL({'scale': 10, 'region': geometry})
                print("Download URL:", url)

                # Download the image from the URL
                response = requests.get(url)

                # Extract files from ZIP archive
                with zipfile.ZipFile(BytesIO(response.content)) as z:
                    z.extractall("downloaded_image")
                    files = z.namelist()
                    print("Extracted files:", files)

                # Helper function to read a single-band TIFF
                def read_band(file_name):
                    with rio.open(f"downloaded_image/{file_name}") as src:
                        return src.read(1)  # Read the first (and only) band

                # Find and read the relevant bands
                red = read_band(next(f for f in files if 'B4' in f))
                green = read_band(next(f for f in files if 'B3' in f))
                blue = read_band(next(f for f in files if 'B2' in f))
                nir = read_band(next(f for f in files if 'B8' in f))

                # Calculate NDVI
                NDVI = (nir - red) / (nir + red + 1e-6)

                # Save NDVI plot to buffer
                plt.figure(figsize=(10, 10))
                plt.imshow(NDVI, cmap='RdYlGn')
                plt.axis('off')
                plt.title('NDVI Map')
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
                buffer.seek(0)

                # Save NDVI plot to the database
                plot = NDVIPlot(title='NDVI Plot')
                plot.image.save('ndvi_plot.png', ContentFile(buffer.read()), save=True)
                buffer.close()

                NDWI = (nir - green) / (nir + green + 1e-6)

                    ####WATER BODEIS
                water_mask = NDWI < 0
                rgb_water = np.zeros((*water_mask.shape, 3))
                rgb_water[water_mask, 2] = 1  # Blue for water

                # Save water detection plot to buffer
                plt.figure(figsize=(10, 10))
                plt.imshow(rgb_water)
                plt.axis('off')
                plt.title('Detected Water Bodies')
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
                buffer.seek(0)

                # Save water plot to the database
                water = Water(title='Water Plot')
                water.image.save('water_plot.png', ContentFile(buffer.read()), save=True)
                buffer.close()
                plt.close()

                return render(request, 'index.html', {'form': form, 'plot': plot, 'water': water})

            except Exception as e:
                print(f"Error processing image: {e}")
                return render(request, 'index.html', {'form': form, 'error': str(e)})

    else:
        form = LocationForm()

    return render(request, 'index.html', {'form': form})
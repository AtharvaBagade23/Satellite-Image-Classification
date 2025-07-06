from django.shortcuts import render, redirect
from .form import TIFFUploadForm
from .models import TIFFImage, NDVIPlot, Water
import rasterio as rio
import numpy as np
from io import BytesIO
from rasterio.plot import reshape_as_image
import matplotlib
import matplotlib.pyplot as plt
from django.core.files.base import ContentFile
from django.contrib import messages

# Use 'Agg' backend for Matplotlib
matplotlib.use('Agg')

def calculate_area(mask, src):
    """Calculate area in square kilometers from a binary mask"""
    # Get pixel dimensions in meters
    transform = src.transform
    pixel_area_m2 = abs(transform[0] * transform[4])
    
    # Convert to km²
    pixel_area_km2 = pixel_area_m2 / 1_000_000
    
    # Count pixels in the mask
    pixel_count = np.sum(mask)
    
    # Calculate total area
    total_area_km2 = pixel_count * pixel_area_km2
    
    return total_area_km2

def index(request):
    if request.method == 'POST':
        form = TIFFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded TIFF file
            uploaded_image = form.save()
            
            try:
                # Open the uploaded TIFF file
                with rio.open(uploaded_image.image.path) as src:
                    img_data = src.read()
                    tiff_image = reshape_as_image(img_data)

                # Extract RGB and NIR channels
                red = tiff_image[:, :, 2] if tiff_image.shape[2] > 2 else None
                green = tiff_image[:, :, 1] if tiff_image.shape[2] > 1 else None
                blue = tiff_image[:, :, 0]
                
                # Create empty objects for vegetation and water
                plot = None
                water = None
                
                # Process NIR band if available
                if tiff_image.shape[2] > 3:
                    nir = tiff_image[:, :, 3]
                    
                    # Calculate NDVI for vegetation
                    NDVI = (nir - red) / (nir + red + 1e-6)
                    
                    # Create vegetation mask (NDVI > 0.2 indicates vegetation)
                    veg_mask = NDVI > 0.2
                    
                    # Calculate vegetation area
                    veg_area_km2 = calculate_area(veg_mask, src)
                    
                    # Save NDVI plot to buffer
                    plt.figure(figsize=(10, 10))
                    ndvi_plot = plt.imshow(NDVI, cmap='RdYlGn_r', vmin=-1, vmax=1)
                    plt.colorbar(ndvi_plot, label='NDVI')
                    plt.axis('off')
                    plt.title(f'Vegetation Map (Area: {veg_area_km2:.2f} km²)')

                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
                    buffer.seek(0)

                    # Save plot to NDVIPlot model
                    plot = NDVIPlot(title='NDVI Plot', area_km2=veg_area_km2)
                    plot.image.save('ndvi_plot.png', ContentFile(buffer.read()), save=True)
                    buffer.close()
                    plt.close()

                    # Calculate NDWI for water bodies (correct formula)
                    NDWI = (green - nir) / (green + nir + 1e-6)
                    
                    # Water is typically NDWI > 0
                    water_mask = NDWI > 0
                    
                    # Calculate water area
                    water_area_km2 = calculate_area(water_mask, src)
                    
                    # Create RGB visualization for water bodies
                    rgb_water = np.zeros((*water_mask.shape, 3))
                    rgb_water[water_mask, 2] = 1  # Blue for water

                    # Plot the water detection map
                    plt.figure(figsize=(10, 10))
                    plt.imshow(rgb_water)
                    plt.axis('off')
                    plt.title(f'Water Bodies (Area: {water_area_km2:.2f} km²)')
                    
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
                    buffer.seek(0)

                    # Save plot to Water model
                    water = Water(title='Water Bodies', area_km2=water_area_km2)
                    water.image.save('water_plot.png', ContentFile(buffer.read()), save=True)
                    buffer.close()
                    plt.close()
                    
                    # Display selected output based on dropdown
                    selected_output = request.POST.get('imagess', 'Vegetation')
                    
                    return render(request, 'index.html', {
                        'form': form, 
                        'water': water, 
                        'plot': plot,
                        'selected_output': selected_output
                    })
                else:
                    messages.error(request, "The uploaded image doesn't have enough bands. Need at least 4 bands including NIR.")
            
            except Exception as e:
                messages.error(request, f"Error processing TIFF file: {e}")
                print(f"Error processing TIFF file: {e}")

    else:
        form = TIFFUploadForm()

    return render(request, 'index.html', {'form': form})

def statistics(request):
    """View to display statistics about processed images"""
    ndvi_data = NDVIPlot.objects.all().order_by('-created_at')[:10]
    water_data = Water.objects.all().order_by('-created_at')[:10]
    
    total_veg_area = sum(plot.area_km2 for plot in ndvi_data)
    total_water_area = sum(water.area_km2 for water in water_data)
    
    # Prepare chart data
    chart_data = {
        'labels': [item.created_at.strftime('%b %d') for item in ndvi_data],
        'vegData': [float(item.area_km2) for item in ndvi_data],
        'waterData': [float(item.area_km2) for item in water_data[:len(ndvi_data)]]  # Match lengths
    }
    
    context = {
        'ndvi_data': ndvi_data,
        'water_data': water_data,
        'total_veg_area': total_veg_area,
        'total_water_area': total_water_area,
        'chart_data': chart_data
    }
    
    return render(request, 'statistics.html', context)
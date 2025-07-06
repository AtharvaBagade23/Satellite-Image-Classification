from django.db import models

class TIFFImage(models.Model):
    title = models.CharField(max_length=200, default="Uploaded Image")
    image = models.FileField(upload_to='tiff_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class NDVIPlot(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ndvi_plots/')
    created_at = models.DateTimeField(auto_now_add=True)
    area_km2 = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.title

class Water(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='water_plots/')
    created_at = models.DateTimeField(auto_now_add=True)
    area_km2 = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.title
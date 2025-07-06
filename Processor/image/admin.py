from django.contrib import admin
from .models import TIFFImage, NDVIPlot, Water

@admin.register(TIFFImage)
class TIFFImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(NDVIPlot)
class NDVIPlotAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'area_km2')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(Water)
class WaterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'area_km2')
    search_fields = ('title',)
    list_filter = ('created_at',)
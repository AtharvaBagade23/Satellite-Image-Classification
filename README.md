# 🌍 Satellite Image Classification & Analysis

A Django web application for processing satellite imagery to analyze vegetation (NDVI) and water bodies using advanced remote sensing techniques.

![Django](https://img.shields.io/badge/Django-5.1.1-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Features

- **🌱 Vegetation Analysis (NDVI)**: Calculate and visualize Normalized Difference Vegetation Index
- **💧 Water Body Detection**: Identify and map water bodies using NDWI
- **📊 Area Calculations**: Automatic calculation of vegetation and water areas in square kilometers
- **📈 Statistics Dashboard**: Track processing history and generate reports
- **🖼️ TIFF File Support**: Process multi-band satellite imagery (Sentinel-2, Landsat, etc.)
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔒 Secure File Upload**: Safe handling of satellite imagery files

## 🛠️ Technology Stack

- **Backend**: Django 5.1.1
- **Python**: 3.11+
- **Image Processing**: Rasterio, NumPy, Matplotlib
- **Machine Learning**: Scikit-learn
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Render, Railway, Heroku ready

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/AtharvaBagade23/Satellite-Image-Classification.git
   cd Satellite-Image-Classification/Processor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   ```
   http://127.0.0.1:8000/
   ```

## 🎯 Usage

### Uploading Satellite Imagery

1. **Prepare your TIFF file**:
   - Must be multi-band satellite imagery (4+ bands recommended)
   - Supported formats: GeoTIFF, TIFF
   - Recommended: Sentinel-2, Landsat imagery

2. **Upload and Process**:
   - Navigate to the home page
   - Click "Choose File" and select your TIFF file
   - Select output type (Vegetation or Water)
   - Click "Upload and Process"

3. **View Results**:
   - NDVI map for vegetation analysis
   - Water body detection map
   - Area calculations in square kilometers
   - Download processed images

### Understanding the Results

- **NDVI Values**:
  - -1 to 1 scale
  - Higher values (0.2+) indicate healthy vegetation
  - Lower values indicate bare soil or water

- **Water Detection**:
  - NDWI > 0 typically indicates water bodies
  - Blue visualization shows detected water areas

## 📊 API Endpoints

- `GET /` - Main upload interface
- `POST /` - File upload and processing
- `GET /statistics/` - Processing statistics and charts
- `GET /admin/` - Django admin interface

## 🔧 Configuration

### Supported Satellite Data

- **Sentinel-2**: 10m resolution, 13 bands
- **Landsat 8/9**: 30m resolution, 11 bands
- **Other multi-band imagery**: Any GeoTIFF with 4+ bands

### File Size Limits

- **Maximum file size**: 100MB (configurable)
- **Recommended**: 50MB or less for faster processing

## 📁 Project Structure

```
Processor/
├── Processor/                 # Django project settings
│   ├── settings.py           # Main settings file
│   ├── urls.py               # URL configuration
│   └── wsgi.py               # WSGI application
├── image/                    # Main app
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # File upload forms
│   ├── templates/            # HTML templates
│   └── static/               # CSS, JS, images
├── media/                    # Uploaded files
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration
├── runtime.txt               # Python version
└── README.md                 # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **502 Bad Gateway Error**:
   - Check Render logs for build errors
   - Verify environment variables are set correctly
   - Ensure `ALLOWED_HOSTS` includes your domain

2. **File Upload Fails**:
   - Check file format (must be TIFF/GeoTIFF)
   - Verify file size (under 100MB)
   - Ensure file has multiple bands

3. **Processing Errors**:
   - Check if TIFF file has sufficient bands (4+ recommended)
   - Verify file is valid satellite imagery
   - Check application logs for specific errors

### Debug Mode

For local debugging, set in `settings.py`:
```python
DEBUG = True
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## 🙏 Acknowledgments

- **Django** - Web framework
- **Rasterio** - Geospatial raster I/O
- **NumPy** - Numerical computing
- **Matplotlib** - Plotting and visualization
- **Scikit-learn** - Machine learning utilities
- **Render** - Deployment platform

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/AtharvaBagade23/Satellite-Image-Classification/issues)
- **Documentation**: [Wiki](https://github.com/AtharvaBagade23/Satellite-Image-Classification/wiki)
- **Email**: your-abagade26@gmail.com

## 🔮 Future Enhancements

- [ ] Support for more satellite data sources
- [ ] Advanced machine learning models
- [ ] Real-time processing
- [ ] API endpoints for programmatic access
- [ ] Mobile app integration
- [ ] Cloud storage integration (AWS S3, Google Cloud)
- [ ] Batch processing capabilities
- [ ] Advanced visualization options


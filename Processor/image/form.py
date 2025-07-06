from django import forms
from .models import TIFFImage

class TIFFUploadForm(forms.ModelForm):
    class Meta:
        model = TIFFImage
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title for the image'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': '.tif,.tiff'})
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.name.split('.')[-1].lower() not in ['tif', 'tiff']:
                raise forms.ValidationError("Only TIFF files are allowed.")
        return image
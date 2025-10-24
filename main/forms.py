from django.forms import ModelForm
from django import forms  # <-- Import this
from main.models import Venue, Article, Events

# --- NEW: Define a class we can apply to all fields ---
form_control_widget = forms.TextInput(attrs={'class': 'form-control'})
form_control_textarea = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
form_control_url = forms.URLInput(attrs={'class': 'form-control'})

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = [
            "name", "city", "address", "contact", "website", 
            "price_range", "facilities", "image_url", "image_url_2", 
            "image_url_3", "image_url_4", "image_url_5"
        ]
        
        # --- NEW: Add this 'widgets' section ---
        widgets = {
            'name': form_control_widget,
            'city': form_control_widget,
            'address': form_control_widget,
            'contact': form_control_widget,
            'website': form_control_url,
            'price_range': form_control_widget,
            'facilities': form_control_textarea,
            'image_url': form_control_url,
            'image_url_2': form_control_url,
            'image_url_3': form_control_url,
            'image_url_4': form_control_url,
            'image_url_5': form_control_url,
        }

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "category", "image_url"]

class EventForm(ModelForm):
    class Meta:
        model = Events
        fields = ["name", "venue", "description", "image_url"]





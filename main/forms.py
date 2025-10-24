from django.forms import ModelForm
from main.models import Venue, Article, Events
from django import forms

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ["name", "city", "address", "contact", "website", "image_url"]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "category", "image_url"]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Blog Post Title'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your blog content here...'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://... (Optional Banner Image)'}),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'category': 'Category',
            'image_url': 'Image URL (Optional)',
        }

class EventForm(ModelForm):
    class Meta:
        model = Events
        fields = ["name", "type", "date", "venue", "price", "description", "image_url"]

        # BLOK "PANJANG" INI...
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Contoh: Morning Fun Match'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}), # <-- Ini yang bikin ada kalender
            'venue': forms.Select(),
            'price': forms.NumberInput(attrs={'placeholder': 'Contoh: 150000'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Event description...'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://... (Opsional)'}),
        }
        
        # ...DAN BLOK INI...
        labels = {
            'name': 'Event Name',
            'type': 'Match Category',
            'date': 'Date & Time',
            'venue': 'Venue',
            'price': 'Price (Rp)',
        }
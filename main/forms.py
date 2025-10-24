from django.forms import ModelForm
from main.models import Venue, Article, Events

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ["name", "city", "address", "contact", "website", "image_url"]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "category", "image_url"]

class EventForm(ModelForm):
    class Meta:
        model = Events
        fields = ["name", "venue", "description", "image_url"]
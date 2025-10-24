from django.urls import path
from main.views import show_main, ajax_article_form, ajax_event_form, ajax_venue_form, register_view, login_view, logout_view, ajax_delete, ajax_edit, ajax_cards, show_article, show_venue, show_event, about_view,rate_item

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('ajax_form/article/', ajax_article_form, name='ajax_article_form'),
    path('ajax_form/event/', ajax_event_form, name='ajax_event_form'),
    path('ajax_form/venue/', ajax_venue_form, name='ajax_venue_form'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('ajax_delete/<str:type>/<uuid:id>/', ajax_delete, name='ajax_delete'),
    path('ajax_edit/<str:type>/<uuid:id>/', ajax_edit, name='ajax_edit'),
    path('ajax_cards/', ajax_cards, name='ajax_cards'),
    path('articles/<uuid:id>', show_article, name='show_article'),
    path('venues/<uuid:id>', show_venue, name='show_venue'),
    path('events/<uuid:id>', show_event, name='show_event'),
    path('about/', about_view, name='about'),
    path('rate/', rate_item, name='rate_item'),
]

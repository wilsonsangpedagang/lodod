from django.urls import path
<<<<<<< HEAD
from . import views  # <-- Import views dengan cara ini
=======
from main.views import show_main, ajax_article_form, ajax_event_form, ajax_venue_form, register_view, login_view, logout_view, ajax_delete, ajax_edit, ajax_cards, show_article, show_venue, show_event, about_view,rate_item
from main.views import (
    show_main, ajax_article_form, ajax_event_form, ajax_venue_form, 
    register_view, login_view, logout_view, ajax_delete, ajax_edit, 
    ajax_cards, show_article, show_venue, show_event, about_view,
    rate_item, show_venues 
)
>>>>>>> tkpbp/radit

app_name = 'main'

urlpatterns = [
<<<<<<< HEAD
    path('', views.show_main, name='show_main'),
    
    # --- URL Ajax untuk Form ---
    # Ini untuk 'main.html' lama
    path('ajax_form/article/', views.ajax_article_form, name='ajax_article_form'),
    path('ajax_form/venue/', views.ajax_venue_form, name='ajax_venue_form'),
    
    # Ini untuk 'event_page.html' baru
    path('ajax_event_form/', views.ajax_event_form, name='ajax_event_form'), 
    
    # --- URL Autentikasi ---
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- URL Ajax CRUD ---
    path('ajax_delete/<str:type>/<uuid:id>/', views.ajax_delete, name='ajax_delete'),
    path('ajax_edit/<str:type>/<uuid:id>/', views.ajax_edit, name='ajax_edit'),
    path('ajax_cards/', views.ajax_cards, name='ajax_cards'),
    
    # --- URL Halaman Detail ---
    path('articles/<uuid:id>', views.show_article, name='show_article'),
    path('venues/<uuid:id>', views.show_venue, name='show_venue'),
    path('events/<uuid:id>', views.show_event, name='show_event'),
    
    # --- URL Halaman Event (Page & Detail Modal) ---
    path('events/', views.event_page, name='event_page'),
    path('ajax_event_detail/<uuid:id>/', views.ajax_event_detail, name='ajax_event_detail'),
    
    # --- URL Lain-lain ---
    path('about/', views.about_view, name='about'),
    path('rate/', views.rate_item, name='rate_item'),

    path('articles/', views.article_list_view, name='article_list'),
    path('articles/<uuid:id>', views.show_article, name='show_article'),
    
    path('ajax_article_form/', views.ajax_article_form, name='ajax_article_form'),
]
=======
    path('', show_main, name='show_main'),
    path('venues/', show_venues, name='show_venues'),
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
    
    # --- THIS IS THE FIX ---
    # Added a trailing slash to match the URL
    path('venues/<uuid:id>/', show_venue, name='show_venue'), 
    
    path('events/<uuid:id>', show_event, name='show_event'),
    path('about/', about_view, name='about'),
    path('rate/', rate_item, name='rate_item'),
]
>>>>>>> tkpbp/radit

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from main.forms import VenueForm, ArticleForm, EventForm
from main.models import Venue, Article, Events
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Avg
from django.contrib.contenttypes.models import ContentType
from main.models import Rating


def show_main(request):
    venues = Venue.objects.all()
    articles = Article.objects.all()
    events = Events.objects.all()
    # Build unified items list
    items = []
    for a in articles:
        avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Article),
        object_id=a.id
        ).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
            'id': a.id,
            'type': 'article',
            'title': a.title,
            'content': a.content,
            'category': a.category,
            'created_at': a.published_date,
            'thumbnail': getattr(a, 'image_url', None),
            'user': getattr(a, 'user', None),
            'detail_url': f"/article/{a.id}/",
            'avg_rating': round(avg_rating, 1),
        })
    for v in venues:
        avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Venue),
        object_id=v.id
        ).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
            'id': v.id,
            'type': 'venue',
            'name': v.name,
            'city': v.city,
            'address': v.address,
            'contact': v.contact,
            'website': v.website,
            'thumbnail': getattr(v, 'image_url', None),
            'user': getattr(v, 'user', None),
            'detail_url': f"/venue/{v.id}/",
            'avg_rating': round(avg_rating, 1),
        })
    for e in events:
        avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Events),
        object_id=e.id
        ).aggregate(avg=Avg('score'))['avg'] or 0
        items.append({
            'id': e.id,
            'type': 'event',
            'name': e.name,
            'description': e.description,
            'date': e.date,
            'venue': e.venue,
            'thumbnail': getattr(e, 'image_url', None),
            'user': getattr(e, 'user', None),
            'detail_url': f"/event/{e.id}/",
            'avg_rating': round(avg_rating, 1),
        })
    # Sort by created_at/date descending
    items.sort(key=lambda x: x.get('created_at', x.get('date', timezone.now())), reverse=True)
    context = {
        'npm': '2206081534',
        'name': 'Roben Joseph',
        'class': 'PBP A',
        'items': items,
        'user': request.user,
    }
    return render(request, "main.html", context)

# Venue views
def create_venue(request):
    form = VenueForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_venue.html", context)

def show_venue(request, id):
    # Get the venue or return 404 if not found
    venue = get_object_or_404(Venue, pk=id)

    # Calculate average rating for this venue
    avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Venue),
        object_id=venue.id
    ).aggregate(avg=Avg('score'))['avg'] or 0

    context = {
        'venue': venue,
        'avg_rating': round(avg_rating, 1),
    }

    return render(request, "venue_detail.html", context)


# Article views
def create_article(request):
    form = ArticleForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        article = form.save(commit=False)
        article.user = request.user   # ✅ attach logged-in user
        article.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_article.html", context)

def show_article(request, id):
    article = get_object_or_404(Article, pk=id)
    avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Article),
        object_id=article.id
    ).aggregate(avg=Avg('score'))['avg'] or 0
    context = {'article': article, 'avg_rating': round(avg_rating, 1)}
    return render(request, "article_detail.html", context)


def ajax_article_form(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors.as_text()})
    else:
        form = ArticleForm()
        html = render_to_string('partials/article_form.html', {'form': form}, request=request)
        return HttpResponse(html)

# Event views
def create_event(request):
    form = EventForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_event.html", context)

def show_event(request, id):
    # Get the event or return 404 if not found
    event = get_object_or_404(Events, pk=id)

    # Calculate average rating for this event
    avg_rating = Rating.objects.filter(
        content_type=ContentType.objects.get_for_model(Events),
        object_id=event.id
    ).aggregate(avg=Avg('score'))['avg'] or 0

    context = {
        'event': event,
        'avg_rating': round(avg_rating, 1),
    }

    return render(request, "event_detail.html", context)


def ajax_event_form(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return JsonResponse({'success': True})  # ✅ Correct placement
        return JsonResponse({'success': False, 'errors': form.errors.as_text()})
    else:
        form = EventForm()
        html = render_to_string('partials/event_form.html', {'form': form}, request=request)
        return HttpResponse(html)


def ajax_venue_form(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.user = request.user
            venue.save()
            return JsonResponse({'success': True})  # ✅ Correct placement
        return JsonResponse({'success': False, 'errors': form.errors.as_text()})
    else:
        form = VenueForm()
        html = render_to_string('partials/venue_form.html', {'form': form}, request=request)
        return HttpResponse(html)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not username or not email or not password:
            return JsonResponse({'success': False, 'errors': 'All fields required.'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'errors': 'Username already exists.'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({'success': True})
    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': 'Invalid credentials.'})
    return render(request, 'login.html')

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('main:show_main')


@csrf_exempt
def ajax_delete(request, type, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'errors': 'Authentication required.'})
    model_map = {'article': Article, 'venue': Venue, 'event': Events}
    model = model_map.get(type)
    if not model:
        return JsonResponse({'success': False, 'errors': 'Invalid type.'})
    obj = get_object_or_404(model, pk=id)
    if hasattr(obj, 'user') and obj.user != request.user:
        return JsonResponse({'success': False, 'errors': 'Permission denied.'})
    obj.delete()
    return JsonResponse({'success': True})

@csrf_exempt
def ajax_edit(request, type, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'errors': 'Authentication required.'})
    model_map = {'article': Article, 'venue': Venue, 'event': Events}
    form_map = {'article': ArticleForm, 'venue': VenueForm, 'event': EventForm}
    model = model_map.get(type)
    form_class = form_map.get(type)
    if not model or not form_class:
        return JsonResponse({'success': False, 'errors': 'Invalid type.'})
    obj = get_object_or_404(model, pk=id)
    if hasattr(obj, 'user') and obj.user != request.user:
        return JsonResponse({'success': False, 'errors': 'Permission denied.'})
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors.as_text()})
    else:
        html = render_to_string(f'partials/{type}_form.html', {'form': form_class(instance=obj)}, request=request)
        return JsonResponse({'html': html})

@csrf_exempt
def ajax_cards(request):
    type_filter = request.GET.get('type', 'all')

    # Fetch all data
    venues = Venue.objects.all()
    articles = Article.objects.all()
    events = Events.objects.all()

    items = []

    # Articles
    if type_filter in ('all', 'article'):
        for a in articles:
            items.append({
                'id': a.id,
                'type': 'article',
                'title': a.title,
                'content': a.content,
                'category': a.category,
                'created_at': a.published_date,
                'thumbnail': getattr(a, 'thumbnail', None) or getattr(a, 'image_url', None),
                'user': a.user,  # ✅ actual user object
                'detail_url': f"/article/{a.id}/",
            })

    # Venues
    if type_filter in ('all', 'venue'):
        for v in venues:
            items.append({
                'id': v.id,
                'type': 'venue',
                'name': v.name,
                'city': v.city,
                'address': v.address,
                'contact': v.contact,
                'website': v.website,
                'thumbnail': getattr(v, 'thumbnail', None) or getattr(v, 'image_url', None),
                'user': v.user,  # ✅ actual user object
                'detail_url': f"/venue/{v.id}/",
            })

    # Events
    if type_filter in ('all', 'event'):
        for e in events:
            items.append({
                'id': e.id,
                'type': 'event',
                'name': e.name,
                'description': e.description,
                'date': e.date,
                'venue': e.venue,
                'thumbnail': getattr(e, 'thumbnail', None) or getattr(e, 'image_url', None),
                'user': e.user,  # ✅ actual user object
                'detail_url': f"/event/{e.id}/",
            })

    # Sort newest first
    items.sort(key=lambda x: x.get('created_at', x.get('date', timezone.now())), reverse=True)

    # Render each card template
    html = "".join([
        render_to_string('card.html', {'item': item, 'user': request.user}, request=request)
        for item in items
    ])
    return HttpResponse(html)


def about_view(request):
    return render(request, "about.html")

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from .models import Rating

@require_POST
@login_required
def rate_item(request):
    item_type = request.POST.get('type')  # 'event', 'venue', 'article'
    item_id = request.POST.get('id')
    score = int(request.POST.get('score'))

    # Determine which model to rate
    model_map = {
        'event': Events,
        'venue': Venue,
        'article': Article
    }

    if item_type not in model_map:
        return JsonResponse({'error': 'Invalid type'}, status=400)

    model = model_map[item_type]
    content_type = ContentType.objects.get_for_model(model)

    # Create or update the rating
    rating, created = Rating.objects.update_or_create(
        user=request.user,
        content_type=content_type,
        object_id=item_id,
        defaults={'score': score},
    )

    # Recalculate average
    avg = Rating.objects.filter(
        content_type=content_type,
        object_id=item_id
    ).aggregate(Avg('score'))['score__avg'] or 0


    return JsonResponse({
        'message': 'Rating saved!',
        'average': round(avg, 1),
        'your_rating': score,
    })

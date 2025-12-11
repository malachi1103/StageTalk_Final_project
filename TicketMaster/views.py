from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Review, Event
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accountRegistration.forms import ProfileForm

TICKETMASTER_API_KEY = "OOoE4TqTjtdRmAG8dayK0SrAUGIKCV0A"

@login_required(login_url='login')
def create_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.event = event
        review.user = request.user
        review.save()
        return redirect('events')
    return render(request, 'reviews/create_review.html', {'form': form, 'event': event})

@login_required(login_url='login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid():
        form.save()
        return redirect('events')
    return render(request, 'reviews/edit_review.html', {'form': form})

@login_required(login_url='login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('events')
    return render(request, 'reviews/delete_review.html', {'review': review})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

@login_required
def upload_profile_picture(request):
    profile = request.user.profile  # assumes you auto-create Profile on signup
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever you want to send them
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accountRegistrations/profilePic.html.html', {'form': form})



def fetch_ticketmaster_events(request):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    search_term = request.GET.get('search_term', '').strip()
    city = request.GET.get('city', '').strip()

    query_parameters = {
        'apikey': TICKETMASTER_API_KEY,
        'sort': 'date,asc',
        'countryCode': 'US',
        'size': 20
    }

    keyword_map = {
        "Music": "concert",
        "Arts & Theatre": "theatre",
        "Miscellaneous": "family",
        "Sports": "sports"
    }

    if search_term:
        query_parameters['keyword'] = keyword_map.get(search_term, search_term)
    else:
        query_parameters['keyword'] = "Taylor Swift"  # fallback keyword

    if city:
        query_parameters['city'] = city

    events = []

    try:
        response = requests.get(base_url, params=query_parameters)
        response.raise_for_status()
        data = response.json()

        if '_embedded' in data and 'events' in data['_embedded']:
            raw_events = data['_embedded']['events']
            for ev in raw_events:
                venue_name, venue_city = None, None
                if '_embedded' in ev and 'venues' in ev['_embedded']:
                    venue = ev['_embedded']['venues'][0]
                    venue_name = venue.get('name')
                    venue_city = venue.get('city', {}).get('name')

                image_url = None
                if 'images' in ev and ev['images']:
                    best_image = max(ev['images'], key=lambda img: img.get('width', 0))
                    image_url = best_image.get('url')

                raw_datetime = ev.get('dates', {}).get('start', {}).get('dateTime')
                parsed_datetime = None
                if raw_datetime:
                    try:
                        parsed_datetime = datetime.strptime(raw_datetime, "%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        parsed_datetime = None

                # Save or get event in local DB
                db_event, created = Event.objects.get_or_create(
                    name=ev.get('name'),
                    venue_name=venue_name,
                    venue_city=venue_city,
                    defaults={
                        'start_date_time': parsed_datetime,
                        'image_url': image_url,
                        'url': ev.get('url')
                    }
                )
                events.append(db_event)

    except Exception:
        pass

    # Fallback: if no Ticketmaster events, show all local DB events
    if not events:
        events = Event.objects.all()

    context = {
        'events_list': events
    }
    return render(request, 'events/results.html', context)


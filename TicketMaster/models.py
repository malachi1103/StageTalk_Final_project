from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_date_time = models.DateTimeField(null=True, blank=True)  # store proper datetime objects
    venue_name = models.CharField(max_length=255, null=True, blank=True)
    venue_city = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ✅ Only one event field, with related_name for reverse lookup
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1–5 star rating
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp when created
    updated_at = models.DateTimeField(auto_now=True)      # auto timestamp when updated

    def __str__(self):
        return f"{self.user.username} - {self.event.name if self.event else 'No Event'} ({self.rating}★)"



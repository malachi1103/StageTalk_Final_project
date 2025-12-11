"""

"""
from django.contrib import admin
from django.urls import path, include
from TicketMaster import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    # Events
    path('events/', views.fetch_ticketmaster_events, name='events'),

    # Reviews (CRUD)
    path('reviews/create/<int:event_id>/', views.create_review, name='create_review'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('reviews/', views.review_list, name='review_list'),

    # Other apps
    path('accountRegistration/', include('accountRegistration.urls')),
    path('products/', include('products.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
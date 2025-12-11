from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        # Only include fields the user should fill out manually
        fields = ['rating', 'comment']
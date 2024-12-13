from django import forms
from .models import Profile
from .models import Plan, Event
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture']
class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description', ]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date']


from django import forms
from authentication.models import User


class SubscriptionForm(forms.Form):
    users = forms.ModelChoiceField(User.objects.all().order_by('username'))



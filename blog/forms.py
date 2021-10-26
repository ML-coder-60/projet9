from django import forms
from blog.models import UserFollows


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['followed_user'].label = ''


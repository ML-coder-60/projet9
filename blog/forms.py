from django import forms
from blog.models import UserFollows, Ticket
from authentication.models import User


class SubscriptionForm(forms.ModelForm):
    subcribe = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserFollows
        fields = ['followed_user']


class UnSubcribeForm(forms.Form):
    unsubcribe = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UserSubcribeForm(forms.ModelForm):
    subcribe = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, exclude, *args, **kwargs):
        super(UserSubcribeForm, self).__init__(*args, **kwargs)
        self.fields['followed_user'].label = ''
        self.fields['followed_user'].queryset = User.objects.all().exclude(id__in=exclude)

    class Meta:
        model = UserFollows
        fields = ['followed_user']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class EditTicketForm(forms.Form):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        exclude = ['user', 'time_created']

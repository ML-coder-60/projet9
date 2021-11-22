from django import forms
from blog.models import UserFollows, Ticket, Review
from authentication.models import User


class SubscriptionForm(forms.ModelForm):
    subscribe = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserFollows
        fields = ['followed_user']


class UnSubscriptionForm(forms.Form):
    unsubscribe = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UserSubscribeForm(forms.ModelForm):
    subscribe = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, exclude, *args, **kwargs):
        super(UserSubscribeForm, self).__init__(*args, **kwargs)
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
    class Meta:
        model = Ticket
        exclude = ['user', 'time_created']


class PostForm(forms.Form):
    post_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ['ticket', 'user', 'time_created']


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class EditReviewForm(forms.Form):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserFollows
from .forms import SubscriptionForm
from authentication.models import User


@login_required
def subscription(request):
    """
        List Mes abonnements et mes abonnés

    """
    subscribe = []

    # list mes abonnements
    my_subscription = [x.followed_user for x in UserFollows.objects.filter(user=request.user.id)]
    # list mes abonnés
    my_subscribers = [x.user for x in UserFollows.objects.filter(followed_user=request.user.id)]

    for user in User.objects.all().order_by('username'):
        if user not in my_subscription and user.username != request.user.username:
            subscribe.append(user.username)

    form = SubscriptionForm()
    return render(
        request,
        'blog/subscription.html',
        {
            'form': form,
            'subscribe': subscribe,
            'my_subscription': my_subscription,
            'my_subscribers': my_subscribers
        }
    )

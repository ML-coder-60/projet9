from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blog.models import UserFollows
from . import forms


@login_required
def subscription(request):
    """
        List Mes abonnements et mes abonnés

    """

    # list mes abonnements
    my_subscription = [x.followed_user for x in UserFollows.objects.filter(user=request.user.id)]
    # list mes abonnés
    my_subscribers = [x.user for x in UserFollows.objects.filter(followed_user=request.user.id)]

    #for user in User.objects.all().order_by('username'):
    #    if user not in my_subscription and user.username != request.user.username:
    #        subscribe.append(user.username)

    form = forms.SubscriptionForm()

    if request.method == 'POST':
        form = forms.SubscriptionForm(request.POST)
        if form.is_valid():
            subscribe = form.save(commit=False)
            # set the uploader to the user before saving the model
            subscribe.user = request.user
            # now we can save
            subscribe.save()
            return redirect('subscription')
        else:
            return render(
                request,
                'blog/subscription.html',
                {
                    'form': form,
                    'my_subscription': my_subscription,
                    'my_subscribers': my_subscribers
                }
            )
    return render(
        request,
        'blog/subscription.html',
        {
            'form': form,
            'my_subscription': my_subscription,
            'my_subscribers': my_subscribers
        }
    )

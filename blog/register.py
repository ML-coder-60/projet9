from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import UserFollows
from blog import forms


@login_required
def subscription(request):
    """
        List Mes abonnements et mes abonnés
        Ajouter un abonnements

    """

    # list mes abonnements
    my_subscription_user = UserFollows.objects.filter(user=request.user.id)
    # list mes abonnés
    my_subscribers = UserFollows.objects.filter(followed_user=request.user.id)

    # list les id user (abonnments possibles)  ( les users - les abonements - l'utilisateur )
    my_subscription_user_id = [x.followed_user_id for x in my_subscription_user]
    my_subscription_user_id.append(request.user.id)
    subcribe = forms.UserSubcribeForm(exclude=my_subscription_user_id)

    unsubcribe = forms.UnSubcribeForm()

    if request.method == 'POST':
        if 'subcribe' in request.POST:
            form = forms.SubscriptionForm(request.POST)
            if form.is_valid():
                subscribe = form.save(commit=False)
                # set the user to the user before saving the model
                subscribe.user = request.user
                # now we can save
                subscribe.save()
            return redirect('subscription')
        if 'unsubcribe' in request.POST:
            form = forms.UnSubcribeForm(request.POST)
            if form.is_valid():
                # select the user/falower_user to the user before del
                unsubscribe = get_object_or_404(
                            UserFollows,
                            user=request.user,
                            followed_user_id=request.POST['followed_user_id']
                            )
                # now we can del
                unsubscribe.delete()
                return redirect('subscription')
            return redirect('subscription')
    return render(
        request,
        'blog/subscription.html',
        {
            'subcribe': subcribe,
            'unsubcribe': unsubcribe,
            'my_subscription': my_subscription_user,
            'my_subscribers': my_subscribers
        }
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from blog import forms
from blog.models import Ticket, Review, UserFollows
from itertools import chain
from django.db.models import Q, Count, CharField, Value


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


@login_required
def new_ticket(request):
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            create_ticket = ticket_form.save(commit=False)
            create_ticket.user = request.user
            create_ticket.time_created = datetime.date
            create_ticket.save()
            return redirect('posts')
        return render(request, 'blog/create_ticket.html', {'ticket_form': ticket_form}, )
    return redirect('posts')


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        update_ticket = forms.EditTicketForm()
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
    context = {'edit_form': edit_form, 'update_ticket': update_ticket, 'ticket': ticket}
    return render(request, 'blog/edit_ticket.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('posts')
    context = {'delete_form': delete_form, 'ticket_name': ticket.title}
    return render(request, 'blog/delete_ticket.html', context=context)


@login_required
def new_review(request):
    if request.method == 'POST':
        if 'post_review' in request.POST:
            review_form = forms.ReviewForm(request.POST)
            if review_form.is_valid():
                create_review = review_form.save(commit=False)
                create_review.user = request.user
                create_review.time_created = datetime.date
                create_review.ticket_id = request.POST['ticket_id']
                create_review.save()
                return redirect('posts')
        if 'ticket_id' in request.POST:
            post_review = forms.PostForm()
            ticket = get_object_or_404(Ticket, id=request.POST['ticket_id'])
            if ticket:
                review_form = forms.ReviewForm()
                context = {
                        'ticket': ticket,
                        'review_form': review_form,
                        'new_review': post_review,
                }
                return render(request, 'blog/create_review.html', context=context)
        else:
            ticket_form = forms.TicketForm(request.POST, request.FILES)
            review_form = forms.ReviewForm(request.POST)
            if ticket_form.is_valid() and review_form.is_valid():
                create_ticket = ticket_form.save(commit=False)
                create_ticket.user = request.user
                create_ticket.time_created = datetime.date
                create_ticket.save()
                ticket = get_object_or_404(Ticket, title=request.POST['title'])
                create_review = review_form.save(commit=False)
                create_review.user = request.user
                create_review.time_created = datetime.date
                create_review.ticket_id = ticket.id
                create_review.save()
                return redirect('posts')
            else:
                context = {'ticket_form': ticket_form, 'review_form': review_form}
                return render(request, 'blog/create_ticket_review.html', context=context)
    return redirect('/')


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    tag_update_review = forms.EditReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
    context = {'edit_form': edit_form, 'tag_update_review': tag_update_review}
    return render(request, 'blog/edit_review.html', context=context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('posts')
    context = {'delete_form': delete_form, 'review_headline': review.headline}
    return render(request, 'blog/delete_review.html', context=context)


@login_required
def feed(request):
    ticket = []
    if request.path == "/posts/":
        ticket = Ticket.objects.filter(user=request.user.id).annotate(
                    content_type=Value('TICKET', CharField()),
                    is_review=Count('review')
                    )
        review = Review.objects.filter(
                    Q(user=request.user.id)
                ).annotate(
                    content_type=Value('REVIEW', CharField())
                )

    if request.path == "/flux/":
        id_subscription_user = [x.followed_user_id for x in UserFollows.objects.filter(user=request.user.id)]
        ticket = Ticket.objects.filter(Q(user=request.user.id) | Q(user__in=id_subscription_user)).annotate(
                content_type=Value('TICKET', CharField()),
                is_review=Count('review')
            )

        review_subscription_user = Review.objects.filter(Q(user__in=id_subscription_user)).annotate(
                    content_type=Value('REVIEW', CharField())
                )
        id_review_subscription_user = [x.user_id for x in review_subscription_user]
        ticket_id = [x.id for x in ticket]

        review = Review.objects.filter(
                    Q(user=request.user.id) |
                    Q(ticket__in=ticket_id) |
                    Q(user__in=id_review_subscription_user)
                ).annotate(
                    content_type=Value('REVIEW', CharField())
                )

    all_ticket = Ticket.objects.all()
    posts = sorted(chain(ticket, review), key=lambda post: post.time_created, reverse=True)

    if request.path == "/posts/":
        return render(request, 'blog/posts.html', context={'posts': posts, 'all_ticket': all_ticket, })
    if request.path == "/flux/":
        return render(request, 'blog/flux.html', context={'posts': posts, 'all_ticket': all_ticket, })

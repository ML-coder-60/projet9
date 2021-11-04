from itertools import chain
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blog.models import Ticket, Review
from django.db.models import CharField, Value


@login_required
def feed(request):
    ticket = Ticket.objects.filter(user=request.user.id)
    ticket = ticket.annotate(content_type=Value('TICKET', CharField()))
    review = Review.objects.filter(user=request.user.id)
    review = review.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(ticket, review),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(
        request,
        'blog/flux.html',
        context={'posts': posts}
    )

from itertools import chain
from django.shortcuts import render
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from blog.models import Ticket, Review
from django.db.models import CharField, Value


@login_required
def feed(request):
    ticket = Ticket.objects.filter(
                user=request.user.id
                ).annotate(
                    content_type=Value('TICKET', CharField()),
                    is_review=Count('review')
                )
    ticket_id = [x.id for x in ticket]

    review = Review.objects.filter(
                    Q(user=request.user.id) |
                    Q(ticket__in=ticket_id)
                ).annotate(content_type=Value('REVIEW', CharField()))

    all_ticket = Ticket.objects.all()

    posts = sorted(
        chain(ticket, review),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(
        request,
        'blog/posts.html',
        context={
            'posts': posts,
            'all_ticket': all_ticket,
        }
    )

import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog import forms
from blog.models import Ticket, Review


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
                ticket_form = forms.TicketForm(instance=ticket)
            else:
                ticket_form = forms.TicketForm()
            review_form = forms.ReviewForm()
            context = {
                    'ticket_form': ticket_form,
                    'review_form': review_form,
                    'ticket': ticket.id,
                    'new_review': post_review,
            }
            return render(request, 'blog/create_review.html', context=context)
        else:
            review_form = forms.ReviewForm(request.POST)
            ticket_form = forms.TicketForm(request.POST)
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
                context = {
                    'ticket_form': ticket_form,
                    'review_form': review_form,
                    }
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
    context = {
        'edit_form': edit_form,
        'tag_update_review': tag_update_review
    }
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
    context = {
        'delete_form': delete_form,
        'review_headline': review.headline
    }
    return render(request, 'blog/delete_review.html', context=context)

import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog import forms
from blog.models import Ticket


@login_required
def new_ticket(request):
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
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
    update_ticket = forms.EditTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
    context = {
        'edit_form': edit_form,
        'edit_ticket': update_ticket
    }
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
    context = {
        'delete_form': delete_form,
        'ticket_name': ticket.title
    }
    return render(request, 'blog/delete_ticket.html', context=context)

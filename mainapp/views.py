from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, TicketSubmission, SendMessage, TicketUpdate, TicketInitiate
from django.contrib import messages
from .models import Ticket, Message
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Account ----

@login_required
def account(request):
    user_tickets = Ticket.objects.filter(participants=request.user)
    recieved_messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')[:5]
    sent_messages = Message.objects.filter(sender=request.user).order_by('-sent_at')[:5]
    if request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            try:
                recipient_id = form.cleaned_data['recipient']
                recipient = get_user_model().objects.get(id=recipient_id.id)
                message = Message(
                    sender=request.user,
                    recipient=recipient,
                    subject=form.cleaned_data['subject'],
                    body=form.cleaned_data['body']
                )
                message.save()
                messages.success(request, "Message Sent" )
                return redirect('account')
            except User.DoesNotExist:
                form.add_error('recipient', 'Recipient does not exist.')
    else:
        recipient_id = request.GET.get('recipient')
        initial_data = {'recipient': recipient_id} if recipient_id else None
        form = SendMessage(initial=initial_data)
        form.fields['recipient'].queryset = get_user_model().objects.exclude(id=request.user.id)

    context = {'user_tickets': user_tickets, 'messages': recieved_messages, 'sent_messages': sent_messages, 'form': form}
    return render(request, 'account/account.html', context)

@login_required
def all_messages(request):
    recieved_messages = Message.objects.filter(recipient=request.user).order_by('-sent_at')
    return render(request, 'account/all_messages.html', {'recieved_messages': recieved_messages}) 

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    return render(request, 'account/sent_messages.html', {'sent_messages': sent_messages})

@login_required
def message_room(request):
    all_users= get_user_model().objects.all().exclude(id=request.user.id)
    if request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            try:
                recipient_id = form.cleaned_data['recipient']
                recipient = get_user_model().objects.get(id=recipient_id.id)
                message = Message(sender=request.user, recipient=recipient, subject=form.cleaned_data['subject'], body=form.cleaned_data['body'])
                message.save()
                messages.success(request, "Message Sent" )
                return redirect('account')
            except User.DoesNotExist:
                form.add_error('recipient', 'Recipient does not exist.')
    else:
        recipient_id = request.GET.get('recipient')
        initial_data = {'recipient': recipient_id} if recipient_id else None
        form = SendMessage(initial=initial_data)
        form.fields['recipient'].queryset = get_user_model().objects.exclude(id=request.user.id)

    return render(request, 'message_room.html', {'all_users': all_users})

# Tickets ----

@login_required
def all_tickets(request):
    tickets = Ticket.objects.all()

    p = Paginator(Ticket.objects.all(), 8)
    page = request.GET.get('page')
    ticket_page = p.get_page(page)

    # Type
    modify_tickets = Ticket.objects.filter(type='Modify').count()
    feature_tickets = Ticket.objects.filter(type='Feature').count()
    bug_tickets = Ticket.objects.filter(type='Bug').count()

    # Status
    active_tickets = Ticket.objects.filter(status='Active').count()
    complete_tickets = Ticket.objects.filter(status='Complete').count()
    backlog_tickets = Ticket.objects. filter(status='Backlog').count()

    #Priority
    high_tickets = Ticket.objects.filter(priority='High').count()
    low_tickets = Ticket.objects. filter(priority='Low').count()

    context = {'ticket_page': ticket_page, 'tickets': tickets, 'modify_tickets': modify_tickets, 'feature_tickets': feature_tickets, 'bug_tickets': bug_tickets, 'active_tickets': active_tickets, 'complete_tickets': complete_tickets, 'backlog_tickets': backlog_tickets, 'high_tickets': high_tickets, 'low_tickets': low_tickets}

    return render(request, 'account/tickets.html', context)

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_details.html', {'ticket': ticket})

@login_required
def ticket_room(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    if request.method == 'POST':
        if 'form-update' in request.POST:
            form_update = TicketUpdate(request.POST, instance=ticket)
            if form_update.is_valid():
                ticket = form_update.save(commit=False)
                comment = form_update.cleaned_data['comments']
                if comment:
                    ticket.add_comments(comment)
                ticket.save()
                messages.success(request, "Ticket Updated" )
                return redirect('ticket-room', pk=ticket.id)
            
        elif 'form-initiate' in request.POST:
            form_initiate = TicketInitiate(request.POST, instance=ticket)
            if form_initiate.is_valid():
                ticket = form_initiate.save(commit=False)
                status = form_initiate.cleaned_data['status']
                if status:
                    ticket.initiate(status)
                ticket.save()
                messages.success(request, "Ticket Initiated")
                return redirect('ticket-room', pk=ticket.id)
    else:
        form_update = TicketUpdate(instance=ticket)
        form_initiate = TicketInitiate(instance=ticket)

    context = {'ticket': ticket, 'form_update': form_update, 'form_initiate': form_initiate}
    return render(request, 'ticket_room.html', context)

@login_required
def ticket_submission(request):
    if request.method == 'POST':
        form = TicketSubmission(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            messages.success(request, "Ticket Submitted")
            return redirect('ticket-submission')
            
    else:
        author_id = request.GET.get('author')
        initial_data = {'author': author_id} if author_id else None
        form = TicketSubmission(initial=initial_data)
        
    return render(request, 'account/ticket_submission.html', {'form': form})

def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    if request.method == 'POST':
        ticket.delete()
        return redirect('all-tickets') 

    return render(request, 'ticket_delete.html', {'ticket': ticket})

# Message ----

@login_required
def message(request, pk):
    message = get_object_or_404(Message, id=pk)
    return render(request, 'message_room.html', {'message': message})


@login_required
def send_message(request):
    ticket = Ticket.objects.all()
    if request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            try:
                recipient_id = get_user_model().objects.all().exclude(id=request.user.id)
                recipient = get_user_model().objects.get(id=recipient_id.id)
                message = Message(
                    sender=request.user,
                    recipient=recipient,
                    subject=form.cleaned_data['subject'],
                    body=form.cleaned_data['body'],
                    ticket_id=ticket.id)
                
                message.save()
                messages.success(request, "Message Sent" )
                return redirect('send-message')
            except User.DoesNotExist:
                form.add_error('recipient', 'Recipient does not exist.')
    else:
        recipient_id = request.GET.get('recipient')
        initial_data = {'recipient': recipient_id} if recipient_id else None
        form = SendMessage(initial=initial_data)
        form.fields['recipient'].queryset = get_user_model().objects.exclude(id=request.user.id)

    context = {'form': form, 'ticket': ticket}
    return render(request, 'account/send_message.html', context)

# Dashboard ----

@login_required
def dashboard(request):
    tickets = Ticket.objects.all()
    recent_ticket = Ticket.objects.filter(participants=request.user).latest('created')
    all_users= get_user_model().objects.all().exclude(id=request.user.id)
    if request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            try:
                recipient_id = form.cleaned_data['recipient']
                recipient = get_user_model().objects.get(id=recipient_id.id)
                message = Message(sender=request.user, recipient=recipient, subject=form.cleaned_data['subject'], body=form.cleaned_data['body'])
                message.save()
                messages.success(request, "Message Sent" )
                return redirect('dashboard')
            except User.DoesNotExist:
                form.add_error('recipient', 'Recipient does not exist.')
    else:
        recipient_id = request.GET.get('recipient')
        initial_data = {'recipient': recipient_id} if recipient_id else None
        form = SendMessage(initial=initial_data)
        form.fields['recipient'].queryset = get_user_model().objects.exclude(id=request.user.id)
    
    context = {'section': 'dashboard', 'tickets': tickets, 'recent_ticket': recent_ticket, 'all_users': all_users, 'form': form}
    return render(request, 'account/dashboard.html', context)

# Login/Logout ----

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    return redirect('dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid login. Please try again')
            
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('login')


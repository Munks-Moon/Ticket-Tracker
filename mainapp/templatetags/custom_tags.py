from django import template
from ..models import Ticket
from django.db.models import Count


register = template.Library()

@register.simple_tag
def total_tickets():
    return Ticket.objects.filter(status='Active').count()

@register.inclusion_tag('account\latest_tickets.html')
def show_latest_tickets(count=5):
    latest_tickets = Ticket.objects.all().order_by('-updated')[:count]
    return {'latest_tickets': latest_tickets}


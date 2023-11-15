from django.contrib import admin
from .models import Ticket, Message

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'participants', 'id', 'status']
    list_filter = ['created', 'updated', 'status']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'recipient', 'sent_at', 'read']
    list_filter = ['sent_at', 'read']
    search_fields = ['subject', 'sender__username', 'recipient__username']
    date_hierarchy = 'sent_at'
    ordering = ['-sent_at']

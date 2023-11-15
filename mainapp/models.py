from django.db import models
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Ticket.Status.ACTIVE)

class Ticket(models.Model):
    
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        COMPLETE = 'Complete', 'Complete'
        BACKLOG = 'Backlog', 'Backlog'


    class Priority(models.TextChoices):
        HIGH = 'High', 'High'
        LOW = 'Low', 'Low'

    class Type(models.TextChoices):
        BUG = 'Bug', 'Bug'
        FEATURE = 'Feature', 'Feature'
        MODIFY = 'Modify', 'Modify'

    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ticket_submission')
    participants = models.ForeignKey(User, on_delete=models.PROTECT, related_name='participants', default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.BUG)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.LOW)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BACKLOG)
    comments = models.TextField(blank=True)
    attachment = models.FileField(upload_to='ticket_attachments/', blank=True, null=True)
    
    objects = models.Manager()
    published = PublishedManager()
    

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.title
    
    def add_comments(self, comment):
        self.comments = comment
        self.save()

    def initiate(self, status):
        self.status = status
        self.save()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    

    def mark_as_read(self):
        self.read = True
        self.save()

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return self.subject

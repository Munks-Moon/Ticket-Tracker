from django import forms
from .models import Ticket, Message
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TicketSubmission(forms.ModelForm):
    
    participants = forms.ModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'author', 'type', 'priority', 'participants', 'attachment']
        widgets = {
            'participants': forms.Select(attrs={'class': 'form-control'}),
        }
        
class SendMessage(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        labels = {
            'subject': 'Subject',
            'body': 'Message',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
        }

class TicketUpdate(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'comments']

class TicketInitiate(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['status']

   
        
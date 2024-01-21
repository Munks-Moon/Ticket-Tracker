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
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'participants': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
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
            'recipient': forms.Select(attrs={'class': 'custom-select', 'style': 'width: 300px;'}),  # Change size and add class
            'subject': forms.TextInput(attrs={'placeholder': 'Enter subject here', 'style': 'width: 200px;'}),  # Add placeholder and change size
            'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your description here'}), 
        }

class TicketUpdate(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'comments']

class TicketInitiate(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']

   
        
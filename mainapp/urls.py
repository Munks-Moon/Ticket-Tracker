from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.user_login, name='login'),
    path('ticket-submit/', views.ticket_submission, name='ticket-submission'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket-room/<str:pk>/', views.ticket_room, name='ticket-room'),
    path('logout/', views.logoutUser, name="logout"),
    path('account/', views.account, name='account'),
    path('all-tickets/', views.all_tickets, name='all-tickets'),
    path('send-message/', views.send_message, name='send-message'),
    path('message-room/<str:pk>/', views.message, name='message'),
    path('all-messages/', views.all_messages, name='all-messages'),
    path('sent-messages/', views.sent_messages, name='sent-messages'),
    path('ticket-room/<str:pk>/delete/', views.delete_ticket, name='ticket-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

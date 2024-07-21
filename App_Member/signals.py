# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import Notification

def check_notifications(sender, user, request, **kwargs):
    # Check for notifications for the logged-in user
    notifications = Notification.objects.filter(user=user, read=False)
    # Display notifications to the user
    for notification in notifications:
        print(notification.message)
    # Mark notifications as read
    notifications.update(read=True)
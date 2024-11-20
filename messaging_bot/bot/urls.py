from django.urls import path
from .views import SendMessageView, IndexView

urlpatterns = [
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('', IndexView.as_view(), name='index'),  # Add this line
]
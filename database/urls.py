from django.urls import path
from .views import MemberListView, MemberDetailView

urlpatterns = [
    path('members/', MemberListView.as_view(), name='member-list'),
    path('members/<int:id>/', MemberDetailView.as_view(), name='member-detail'),
]
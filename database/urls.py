from django.urls import path
from .views import MemberListView, MemberDetailView, research4life_redirect

urlpatterns = [
    path('api/members/', MemberListView.as_view(), name='member-list'),
    path('api/members/<int:id>/', MemberDetailView.as_view(), name='member-detail'),
    path('r4l/', research4life_redirect, name='research4life_redirect')
]
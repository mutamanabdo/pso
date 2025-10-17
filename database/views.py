from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Member
from .serializers import MemberSerializer
from rest_framework.filters import SearchFilter
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

#custom automatic r4l login
@login_required(login_url='/admin/login/')  # Redirect to admin login if not authenticated
def research4life_access(request):
    context = {
        'username': settings.RESEARCH4LIFE_USERNAME,
        'password': settings.RESEARCH4LIFE_PASSWORD,
        'login_url': 'https://login.research4life.org/tacgw/login.cshtml',
    }
    return render(request, 'research4life_auto_login.html', context)

# Custom Pagination Class
class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# List and Create View with Filtering and Pagination
class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sex', 'age', 'colleage']  # Exact match filters
    search_fields = ['name', 'email', 'phone_number']  # Searchable fields

# Retrieve, Update, Delete View
class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'id'
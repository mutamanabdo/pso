from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'age', 'phone_number', 'email', 'date_of_join')
    list_filter = ('sex', 'age', 'colleage', 'date_of_join')
    search_fields = ('name', 'email', 'phone_number', 'telegram_id')
    ordering = ('-date_of_join',)
    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'sex', 'age', 'email')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'telegram_id', 'telgram_username')
        }),
        ('Other Details', {
            'fields': ('address', 'colleage', 'working_untill', 'date_of_join', 'is_revision')
        }),
    )
admin.site.register(Member, MemberAdmin)

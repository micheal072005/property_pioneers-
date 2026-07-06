# admin.py
from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message', 'subject']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    ordering = ['-created_at']

    # Beautiful colors
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Client Messages Inbox'}
        return super().changelist_view(request, extra_context)

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} message(s) marked as read")
    mark_as_read.short_description = "Mark as Read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark as Unread"
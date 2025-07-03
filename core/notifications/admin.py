from django.contrib import admin

# Register your models here.
from core.notifications.models import Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('title', 'message')
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        return False
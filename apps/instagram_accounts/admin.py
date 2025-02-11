from django.contrib import admin
from .models import InstagramAccount, ReelUploadTask

@admin.register(InstagramAccount)
class InstagramAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "username", "added_at", "updated_at")
    search_fields = ("username", "user__username")
    list_filter = ("added_at",)


@admin.register(ReelUploadTask)
class ReelUploadTaskAdmin(admin.ModelAdmin):
    list_display = ("account", "upload_option", "schedule_type", "scheduled_time", "status", "created_at")
    search_fields = ("account__username", "upload_option")
    list_filter = ("upload_option", "schedule_type", "status")


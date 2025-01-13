# apps/authentication/admin.py
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth.models import User
from apps.authentication.models import UserProfile
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'expire_date')
    search_fields = ['session_key']

    def user(self, obj):
        try:
            data = obj.get_decoded()
            if '_auth_user_id' in data:
                return User.objects.get(id=data['_auth_user_id'])
        except Exception:
            return None

    def expire_date(self, obj):
        return obj.expire_date

admin.site.register(Session, SessionAdmin)
admin.site.register(UserProfile)

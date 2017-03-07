from django.contrib import admin

from api_keys_server.models import APIKey


class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['mail','api_key','requests']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['api_key','requests']
        else:
            return []


admin.site.register(APIKey, APIKeyAdmin)

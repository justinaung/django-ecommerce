from django.contrib import admin

from django_ecommerce.payments.models import User


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User


admin.site.register(User, UserAdmin)

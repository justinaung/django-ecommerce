from django.contrib import admin

from django_ecommerce.contact.models import ContactForm


class ContactFormAdmin(admin.ModelAdmin):
    class Meta:
        model = ContactForm


admin.site.register(ContactForm, ContactFormAdmin)

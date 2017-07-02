from django import forms

from django_ecommerce.contact.models import ContactForm


class ContactView(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'topic', 'message']
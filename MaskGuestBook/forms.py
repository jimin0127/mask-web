from django import forms
from .models import GuestBook

class GuestBookForm(forms.ModelForm):
    class Meta:
        model = GuestBook
        fields = ('name', 'phone', 'message')

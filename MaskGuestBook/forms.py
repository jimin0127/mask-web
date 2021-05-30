from django import forms
from .models import GuestBookModel

class GuestBookForm(forms.ModelForm):
    class Meta:
        model = GuestBookModel
        fields = ('name','phone', 'message')

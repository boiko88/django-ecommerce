from django.forms import ModelForm
from django import forms

from .models import CustomerComments


class CommentForm(ModelForm):
    class Meta:
        model = CustomerComments
        fields = '__all__'

from django.forms import ModelForm
from .models import CustomerComments
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = CustomerComments
        fields = '__all__'

from django import forms

from .models import CardCollection, Card


class CardCollectionForm(forms.ModelForm):
    class Meta:
        model = CardCollection
        fields = ['title']


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['first_page', 'second_page']
        widgets = {
            'first_page': forms.Textarea(attrs={'rows': 3}),
            'second_page': forms.Textarea(attrs={'rows': 3}),
        }
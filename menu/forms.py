from django import forms

from .models import Menu, Item


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all())
    expiration_day = forms.DateField(widget=forms.SelectDateWidget(years=range(2018, 2023)))

    class Meta:
        model = Menu
        exclude = ('created_day',)

    def clean_season(self):
        season = self.cleaned_data.get('season')
        if not season:
            raise forms.ValidationError("A season name is required.")
        return season

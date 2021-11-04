from django import forms
from .models import Documents, Team, Player
from bootstrap_datepicker_plus import DatePickerInput


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Team
        fields = ('team', 'establishment_date', 'price', 'players', 'league', )
        widgets = {
            'establishment_date': DatePickerInput(format='%Y-%m-%d'),
        }


class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].empty_label = None
        if kwargs.get('instance') is None:
            self.fields['email'].help_text = 'email format: address@host.ext'

    class Meta:
        model = Player
        fields = ('team', 'username', 'email', 'date_bought', )
        widgets = {
            'date_sent': DatePickerInput(format='%Y-%m-%d'),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('file', )


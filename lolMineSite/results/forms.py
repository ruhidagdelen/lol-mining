from django import forms
from .models import PlayerSearch

class PlayerForm(forms.ModelForm):
	class Meta:
		model = PlayerSearch
		fields = ('username','main_role','secondary_role',
			'aggOverFar',
			'aggOverSur',
			'aggOverVis',
			'farOverSur',
			'farOverVis',
			'surOverVis')

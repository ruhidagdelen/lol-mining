from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = ('username','main_role','secondary_role')
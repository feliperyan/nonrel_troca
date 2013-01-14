from django import forms
from nonrel_troca_app.models import GenericItem

class GenericItemForm(forms.Form):
	title = forms.CharField(max_length=100)
	description = forms.CharField(max_length=100)
	value = forms.IntegerField()
	#location = forms.CharField(max_length=100)
	
# Here we use a dummy `queryset`, because ModelChoiceField
# see: http://stackoverflow.com/questions/4789466/populate-a-django-form-with-data-from-database-in-view
class MakeOfferForm(forms.Form):
	itemsToOffer = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=GenericItem.objects.none())
	title = forms.CharField(max_length = 100)

	def __init__(self, user_id):
		super(MakeOfferForm, self).__init__()
		self.fields['itemsToOffer'].queryset = GenericItem.objects.filter(owner_id = user_id)



class GenericServiceForm(GenericItemForm):
	lengthOfEngagement = forms.IntegerField()
	meetUpAddress = forms.CharField(max_length=100) 


class LanguageExchangeForm(GenericServiceForm):
	languageOffered = forms.CharField(max_length=100)
	

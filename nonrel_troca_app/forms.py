from django import forms
from nonrel_troca_app.models import GenericItem
from nonrel_troca_app.models import Book
from nonrel_troca_app.models import Camera
from django.forms import ModelForm


class ModelFormGenericItem(ModelForm):
    class Meta:
        model = GenericItem
        fields = ('title', 'value', 'description')


class ModelFormBook(ModelFormGenericItem):
    class Meta:
        model = Book
        fields = ('title', 'book_author', 'value', 'description')

class ModelFormCameras(ModelFormGenericItem):
    class Meta:
        model = Camera
        fields = ('title', 'brand_name', 'value', 'description')


# Here we use a dummy `queryset`, because ModelChoiceField
# see: http://stackoverflow.com/questions/4789466/populate-a-django-form-with-data-from-database-in-view
class MakeOfferForm(forms.Form):
    itemsToOffer = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=GenericItem.objects.none())
    title = forms.CharField(max_length = 100)

    def __init__(self, user_id):
        super(MakeOfferForm, self).__init__()
        self.fields['itemsToOffer'].queryset = GenericItem.objects.filter(owner_id = user_id)

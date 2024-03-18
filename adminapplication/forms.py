from owner.models import Category,Item,Deadstock_Item
from django import forms
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields='__all__'

class DeadstockItemForm(forms.ModelForm):
    class Meta:
        model=Deadstock_Item
        fields='__all__'
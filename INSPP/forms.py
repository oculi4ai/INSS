
from django import forms
from .models import *


class AddUnpackedProductForm(forms.ModelForm):
    class Meta:
        model=UnpackedProduct
        fields=('name','code','material_type','quantity','unit')
        

class AddRawMaterialForm(forms.ModelForm):

    class Meta:
        model=RawMaterial
        fields=('name','m_type','code','quantity','unit','density','loq_warning','loq_quantity','loq_unit')
        
class AddRawMaterialsInputForm(forms.ModelForm):
    class Meta:
        model=RawMaterialsInput
        fields=('material','quantity','unit','date','note')
        

class AddRawMaterialsOutputForm(forms.ModelForm):
    class Meta:
        model=RawMaterialsOutput
        fields=('material','quantity','unit','date','note')



class AddUnpackedProductRawMaterialForm(forms.ModelForm):
    class Meta:
        model=UnpackedProductRawMaterial
        fields=('product','material','percent')
        


class AddPackedProductForm(forms.ModelForm):
    class Meta:
        model=PackedProduct
        fields=('name','code','unpacked_product','unpacked_product_quantity_in_one','unit')



class AddPackingMaterialForm(forms.ModelForm):

    loq_warning = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model=PackingMaterial
        fields=('name','code','quantity','unit','loq_warning','loq_quantity')    




class AddPackingMaterialOutputForm(forms.ModelForm):

    class Meta:
        model=PackingMaterialOutput
        fields=('material','quantity','date','note')



class AddPackingMaterialInputForm(forms.ModelForm):

    class Meta:
        model=PackingMaterialInput
        fields=('material','quantity','date','note')




class AddPackedProductPackingMaterialForm(forms.ModelForm):

    class Meta:
        model=PackedProductPackingMaterial
        fields=('packed_product','packing_material','count')
        


class AddOrderForm(forms.ModelForm):

    done = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxInput,
    )
    

    starting_date           = forms.DateField(widget=forms.SelectDateWidget)
    planned_finishing_date  = forms.DateField(widget=forms.SelectDateWidget)
    actual_finishing_date   = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model=Order
        fields=('name','code','packed_product','quantity','starting_date','planned_finishing_date','actual_finishing_date')
        

class INSPP_logs_form(forms.ModelForm):

    class Meta:
        model=INSPP_logs
        fields=('operation','table','values','date_and_time','distribution')
        



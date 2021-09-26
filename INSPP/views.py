from django.shortcuts import render,redirect, HttpResponse
from .forms import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.views.generic import ListView ,DetailView

from django.core import serializers
from ServerController.forms import select_model_name
from django.http import JsonResponse
from INSServer import settings


def INSPP_home(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        data={
            'RAWMATERIALS':                 RawMaterial.objects.all(),
            'PACKINGMATERIAL':              PackingMaterial.objects.all(),
            'UNPACKEDPRODUCT':              UnpackedProduct.objects.all(),
            'PACKEDPRODUCT':                PackedProduct.objects.all(),
            'ORDER':                        Order.objects.all(),
        }
        return render(request , 'INSPP_home.html', data)






models_from_name = {
'RAWMATERIALS':                  RawMaterial,
'RAWMATERIALSOUTPUT':           RawMaterialsOutput,
'RAWMATERIALSINPUT':            RawMaterialsInput,
'PACKINGMATERIAL':              PackingMaterial,
'PACKINGMATERIALOUTPUT':        PackingMaterialOutput,
'PACKINGMATERIALINPUT':         PackingMaterialInput,
'UNPACKEDPRODUCT':              UnpackedProduct,
'UNPACKEDPRODUCTRAWMATERIAL':   UnpackedProductRawMaterial,
'PACKEDPRODUCT':                PackedProduct,
'PACKEDPRODUCTPACKINGMATERIAL': PackedProductPackingMaterial,
'ORDER':                        Order,
}


def INSPP_view_data(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            model_name = select_model_name(request.POST ).data['name'].upper()
            model = models_from_name[model_name]
            json_data = model.objects.all()
            serialized_queryset = serializers.serialize('json', json_data)
            json_data=[]
            
            for bit in json.loads(serialized_queryset):
                json_data.append([bit['pk'],]+list(bit['fields'].values()))
            
            try:
                
                request.COOKIES.get('app')
                settings.UPDATED_DATA['INSPP'][model_name] = settings.UPDATED_DATA['INSPP'][model_name]+(request.user,)
            except:
                pass

            return JsonResponse(json_data, safe=False)


        else:
            return render(request, 'get_model_name.html', {'form': select_model_name(),})

    
def INSPP_view_update(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        updated_tables=[]
        for table in settings.UPDATED_DATA['INSPP'].keys():
            if request.user not in settings.UPDATED_DATA['INSPP'][table]:
                updated_tables.append(table)

        if len(json.loads(request.user.profile.new_mail_inbox))>0 or len(json.loads(request.user.profile.new_mail_outbox))>0 or len(json.loads(request.user.profile.mail_edited))>0:
            updated_tables.append('mail')
        

        return JsonResponse(updated_tables, safe=False)



class RawMaterialsView(ListView):
	model 		        = RawMaterial
	context_object_name = 'RawMaterials'
	template_name       = 'RawMaterials.html'
	paginate_by         = 12

class UnpackedProductsView(ListView):
	model 		        = UnpackedProduct
	context_object_name = 'UnpackedProducts'
	template_name       = 'UnpackedProducts.html'
	paginate_by         = 12

class PackedProductsView(ListView):
	model 		        = PackedProduct
	context_object_name = 'PackedProducts'
	template_name       = 'PackedProducts.html'
	paginate_by         = 12

class PackingMaterialsView(ListView):
	model 		        = PackingMaterial
	context_object_name = 'PackingMaterials'
	template_name       = 'PackingMaterials.html'
	paginate_by         = 12

class OrdersView(ListView):
	model 		        = Order
	context_object_name = 'Orders'
	template_name       = 'Orders.html'
	paginate_by         = 12




####################################################
###############     Add         ####################
####################################################



def AddRawMaterial(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        Gas_units=('ML','CL','DL','DAL','KL','T')
        Solid_unis=['MG','CG','DG','DAG','KG',]
        units={
            'SOLID':Solid_unis,
            'LIQUID':Gas_units,
            'GAS':Gas_units
        }

        if request.method =='POST':
            form = AddRawMaterialForm(request.POST or None , request.FILES)
            
            if form.is_valid() and form.data['unit'] in units[form.data['m_type'].upper()] :
                form.save()

                form = AddRawMaterialForm()
                ret = render(request , 'AddRawMaterialForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)
                ret.set_cookie(key ='id', value = RawMaterial.objects.latest('pk').pk)

                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['RAWMATERIALS'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['RAWMATERIALS'] = ()

                return ret
            else:
                
                ret = render(request , 'AddRawMaterialForm.html',{'form':form} )
                if form.data['unit'] not in units[form.data['m_type'].upper()] :
                    ret.set_cookie(key ='message', value = '0')
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddRawMaterialForm()
            ret = render(request , 'AddRawMaterialForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret

def AddRawMaterialsInput(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        Solid_unis=('MG','CG','DG','G','DAG','HG','KG','T')
        Gas_units=['ML','CL','DL','L','DAL','HL','KL']
        units={
            'SOLID':Solid_unis,
            'LIQUID':Gas_units,
            'GAS':Gas_units
        }
        if request.method =='POST':
            
            form = AddRawMaterialsInputForm(request.POST or None , request.FILES)
            if form.is_valid() and form.data['unit'] in units[RawMaterial.objects.get(pk=form.data['material']).m_type.upper()] :
                form.save()

                form = AddRawMaterialsInputForm()
                ret = render(request , 'AddRawMaterialInputForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)
                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['RAWMATERIALSINPUT'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['RAWMATERIALSINPUT'] = ()
                return ret
            else:
                
                ret = render(request , 'AddRawMaterialInputForm.html',{'form':form} )
                if form.data['unit'] not in units[RawMaterial.objects.get(pk=form.data['material']).m_type.upper()] :
                    ret.set_cookie(key ='message', value = '0')
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddRawMaterialsInputForm()
            ret = render(request , 'AddRawMaterialInputForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret



def AddRawMaterialsOutput(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        Solid_unis=('MG','CG','DG','G','DAG','HG','KG','T')
        Gas_units=['ML','CL','DL','L','DAL','HL','KL']
        units={
            'SOLID':Solid_unis,
            'LIQUID':Gas_units,
            'GAS':Gas_units
        }
        if request.method =='POST':
            
            form = AddRawMaterialsOutputForm(request.POST or None , request.FILES)
            if form.is_valid() and form.data['unit'] in units[RawMaterial.objects.get(pk=form.data['material']).m_type.upper()] :
                form.save()

                form = AddRawMaterialsOutputForm()
                ret = render(request , 'AddRawMaterialOutputForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)

                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['RAWMATERIALSOUTPUT'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['RAWMATERIALSOUTPUT'] = ()

                return ret
            else:
                
                ret = render(request , 'AddRawMaterialOutputForm.html',{'form':form} )
                if form.data['unit'] not in units[RawMaterial.objects.get(pk=form.data['material']).m_type.upper()] :
                    ret.set_cookie(key ='message', value = '0')
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddRawMaterialsInputForm()
            ret = render(request , 'AddRawMaterialOutputForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret



def AddUnpackedProduct(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        Gas_units=['ML','CL','DL','L','DAL','HL','KL'],
        Solid_unis=['MG','CG','DG','G','DAG','HG','KG','T'],
        units={
            'SOLID':Solid_unis,
            'LIQUID':Gas_units,
            'GAS':Gas_units
        }

        if request.method =='POST':
            form = AddUnpackedProductForm(request.POST or None , request.FILES)
            if form.is_valid() and form.data['unit'] in units[form.data['material_type'].upper()][0] :
                form.save()


                ret = render(request , 'AddUnpackedProductForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)
                ret.set_cookie(key ='id', value = UnpackedProduct.objects.latest('pk').pk)
                            
                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCT'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCT'] = ()

                return ret
            else:
                ret = render(request , 'AddUnpackedProductForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddUnpackedProductForm()
            ret = render(request , 'AddUnpackedProductForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret


def AddUnpackedProductRawMaterial(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            form = AddUnpackedProductRawMaterialForm(request.POST or None , request.FILES)
            if form.is_valid():
                form.save()


                ret = render(request , 'AddUnpackedProductRawMaterialForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)
                
                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCTRAWMATERIAL'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCTRAWMATERIAL'] = ()

                return ret
            else:
                ret = render(request , 'AddUnpackedProductRawMaterialForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddUnpackedProductRawMaterialForm()
            ret = render(request , 'AddUnpackedProductRawMaterialForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret



def AddPackedProduct(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            form = AddPackedProductForm(request.POST or None , request.FILES)
            if form.is_valid():
                form.save()


                ret = render(request , 'AddPackedProductForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)
                ret.set_cookie(key ='id', value = PackedProduct.objects.latest('pk').pk)

                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['PACKEDPRODUCT'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['PACKEDPRODUCT'] = ()

                return ret
            else:
                ret = render(request , 'AddPackedProductForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddPackedProductForm()
            ret = render(request , 'AddPackedProductForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret



def AddPackingMaterial(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            form = AddPackingMaterialForm(request.POST or None , request.FILES)
            if form.is_valid():
                form.save()


                ret = render(request , 'AddPackingMaterialForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)
                ret.set_cookie(key ='id', value = PackingMaterial.objects.latest('pk').pk)

                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['PACKINGMATERIAL'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['PACKINGMATERIAL'] = ()

                return ret
            else:
                ret = render(request , 'AddPackingMaterialForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddPackingMaterialForm()
            ret = render(request , 'AddPackingMaterialForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret


def AddPackingMaterialOutput(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            form = AddPackingMaterialOutputForm(request.POST or None , request.FILES)
            if form.is_valid():
                form.save()


                ret = render(request , 'AddPackingMaterialOutputForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)

                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['PACKINGMATERIALOUTPUT'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['PACKINGMATERIALOUTPUT'] = ()

                return ret
            else:
                ret = render(request , 'AddPackingMaterialOutputForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddPackingMaterialOutputForm()
            ret = render(request , 'AddPackingMaterialOutputForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret


def AddPackingMaterialInput(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            form = AddPackingMaterialInputForm(request.POST or None , request.FILES)
            if form.is_valid():
                form.save()


                ret = render(request , 'AddPackingMaterialInputForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)

                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['PACKINGMATERIALINPUT'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['PACKINGMATERIALINPUT'] = ()


                return ret
            else:
                ret = render(request , 'AddPackingMaterialInputForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddPackingMaterialInputForm()
            ret = render(request , 'AddPackingMaterialInputForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret


def AddPackedProductPackingMaterial(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            form = AddPackedProductPackingMaterialForm(request.POST or None , request.FILES)
            if form.is_valid():
                form.save()


                ret = render(request , 'AddPackedProductPackingMaterialForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)

                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['PACKEDPRODUCTPACKINGMATERIAL'] = (request.user,)
                else:
                    settings.UPDATED_DATA['INSPP']['PACKEDPRODUCTPACKINGMATERIAL'] = ()
                return ret
            else:
                ret = render(request , 'AddPackedProductPackingMaterialForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddPackedProductPackingMaterialForm()
            ret = render(request , 'AddPackedProductPackingMaterialForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret





def AddOrder(request):
    if not request.user.is_authenticated:
   	    return redirect('login')
    else:
        if request.method =='POST':
            form = AddOrderForm(request.POST or None , request.FILES)
            print(form.errors)
            form.done = request.POST['done']
            if form.is_valid():
                form.save()


                ret = render(request , 'AddOrderForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 1)
                if request.COOKIES.get('app') !=None:
                    settings.UPDATED_DATA['INSPP']['ORDER'] = (request.user,)
                    
                else:
                    settings.UPDATED_DATA['INSPP']['ORDER'] = ()
                return ret
            else:
                ret = render(request , 'AddOrderForm.html',{'form':form} )
                ret.set_cookie(key ='status', value = 0)
                return ret


            
        else:
            form = AddOrderForm()
            ret = render(request , 'AddOrderForm.html',{'form':form} )
            ret.set_cookie(key ='status', value = 0)
            return ret




####################################################
###############     Edit        ####################
####################################################


class RawMaterialView(DetailView):
    model 		= RawMaterial

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            rm=RawMaterial.objects.get(pk=self.kwargs['pk'])
            context = super(RawMaterialView, self).get_context_data(**kwargs)
            form =AddRawMaterialForm(instance=rm)
            context['form'] = form
            return context
    
    def post(self, request, *args, **kwargs):
   	    if 'edit' in request.POST:
   	        rm=RawMaterial.objects.get(pk=self.kwargs['pk'])
   	        form = AddRawMaterialForm(request.POST, request.FILES , instance=rm)			
   	        if form.is_valid():
   	            form.save()

   	            if request.COOKIES.get('app') !=None:
   	                settings.UPDATED_DATA['INSPP']['RAWMATERIALS'] = (request.user,)
   	            else:
   	                settings.UPDATED_DATA['INSPP']['RAWMATERIALS'] = ()

   	        return redirect('EditRawMaterial', rm.pk)
   	    elif 'delete' in request.POST:
   	        rm=RawMaterial.objects.get(pk=self.kwargs['pk'])
   	        rm.delete()
   	        if request.COOKIES.get('app') !=None:
   	            settings.UPDATED_DATA['INSPP']['RAWMATERIALS'] = (request.user,)
   	        else:
   	            settings.UPDATED_DATA['INSPP']['RAWMATERIALS'] = ()

   	        return redirect('INSPPHome')
            


class PackingMaterialView(DetailView):
   	model 		= PackingMaterial

   	def get_context_data(self, **kwargs):
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')
   	    else:
   	        pm=PackingMaterial.objects.get(pk=self.kwargs['pk'])
   	        context = super(PackingMaterialView, self).get_context_data(**kwargs)
   	        form =AddPackingMaterialForm(instance=pm)
   	        context['form'] = form
   	        return context
    
   	def post(self, request, *args, **kwargs):
   	    
   	    if 'edit' in request.POST:
   	        pm=PackingMaterial.objects.get(pk=self.kwargs['pk'])
   	        form = AddPackingMaterialForm(request.POST, request.FILES , instance=pm)			
   	        if form.is_valid():
   	            form.save()

   	            if request.COOKIES.get('app') !=None:
   	                settings.UPDATED_DATA['INSPP']['PACKINGMATERIAL'] = (request.user,)
   	            else:
   	                settings.UPDATED_DATA['INSPP']['PACKINGMATERIAL'] = ()

   	        return redirect('EditPackingMaterial', pm.pk)

   	    elif 'delete' in request.POST:
   	        pm=PackingMaterial.objects.get(pk=self.kwargs['pk'])   	        
   	        pm.delete()

   	        if request.COOKIES.get('app') !=None:
   	            settings.UPDATED_DATA['INSPP']['PACKINGMATERIAL'] = (request.user,)
   	        else:
   	            settings.UPDATED_DATA['INSPP']['PACKINGMATERIAL'] = ()

   	        return redirect('INSPPHome')

   	 
        


class UnpackedProductView(DetailView):
   	model 		= UnpackedProduct

   	def get_context_data(self, **kwargs):
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')
   	    else:
   	        upp=UnpackedProduct.objects.get(pk=self.kwargs['pk'])
   	        context = super(UnpackedProductView, self).get_context_data(**kwargs)
   	        form =AddUnpackedProductForm(instance=upp)
   	        context['form'] = form
   	        return context
        
   	def post(self, request, *args, **kwargs):
   	    
   	    if 'edit' in request.POST:
   	        upp=UnpackedProduct.objects.get(pk=self.kwargs['pk'])
   	        form = AddUnpackedProductForm(request.POST, request.FILES , instance=upp)			
   	        if form.is_valid():
   	            form.save()

   	            if request.COOKIES.get('app') !=None:
   	                settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCT'] = (request.user,)
   	            else:
   	                settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCT'] = ()

   	        return redirect('EditUnpackedProduct', upp.pk)

   	    elif 'delete' in request.POST:
   	        upp=UnpackedProduct.objects.get(pk=self.kwargs['pk'])  	        
   	        upp.delete()

   	        if request.COOKIES.get('app') !=None:
   	            settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCT'] = (request.user,)
   	        else:
   	            settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCT'] = ()

   	        return redirect('INSPPHome')
   	    else:
   	        return redirect('INSPPHome')
        

class UnpackedProductRawMaterialView(DetailView):
   	model 		= UnpackedProductRawMaterial

   	def get_context_data(self, **kwargs):
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')
   	    else:
   	        upprm=UnpackedProductRawMaterial.objects.get(pk=self.kwargs['pk'])
   	        context = super(UnpackedProductRawMaterialView, self).get_context_data(**kwargs)
   	        form =AddUnpackedProductRawMaterialForm(instance=upprm)
   	        context['form'] = form
   	        return context
    
   	def post(self, request, *args, **kwargs):
   	    if 'edit' in request.POST:
   	        upprm=UnpackedProductRawMaterial.objects.get(pk=self.kwargs['pk'])
   	        form = AddUnpackedProductRawMaterialForm(request.POST, request.FILES , instance=upprm)			
   	        if form.is_valid():
   	            form.save()

   	            if request.COOKIES.get('app') !=None:
   	                settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCTRAWMATERIAL'] = (request.user,)
   	            else:
   	                settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCTRAWMATERIAL'] = ()

   	        return redirect('EditUnpackedProductRawMaterial', upprm.pk)

   	    elif 'delete' in request.POST:
   	        upprm=UnpackedProductRawMaterial.objects.get(pk=self.kwargs['pk'])
   	        upprm.delete()
   	        if request.COOKIES.get('app') !=None:
   	            settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCTRAWMATERIAL'] = (request.user,)
   	        else:
   	            settings.UPDATED_DATA['INSPP']['UNPACKEDPRODUCTRAWMATERIAL'] = ()
   	        return redirect('INSPPHome')
        


class PackedProductView(DetailView):
   	model 		= PackedProduct

   	def get_context_data(self, **kwargs):
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')
   	    else:
   	        pp=PackedProduct.objects.get(pk=self.kwargs['pk'])
   	        context = super(PackedProductView, self).get_context_data(**kwargs)
   	        form =AddPackedProductForm(instance=pp)
   	        context['form'] = form
   	        context['object'] = pp
   	        return context
        
   	def post(self, request, *args, **kwargs):

   	    if 'edit' in request.POST:
   	        pp=PackedProduct.objects.get(pk=self.kwargs['pk'])
   	        form = AddPackedProductForm(request.POST, request.FILES , instance=pp)			
   	        if form.is_valid():
   	            form.save()

   	            if request.COOKIES.get('app') !=None:
   	                settings.UPDATED_DATA['INSPP']['PACKEDPRODUCT'] = (request.user,)
   	            else:
   	                settings.UPDATED_DATA['INSPP']['PACKEDPRODUCT'] = ()

   	        return redirect('EditPackedProduct', pp.pk)


   	    elif 'delete' in request.POST:
   	        pp=PackedProduct.objects.get(pk=self.kwargs['pk'])
   	        pp.delete()
            
   	        if request.COOKIES.get('app') !=None:
   	            settings.UPDATED_DATA['INSPP']['PACKEDPRODUCT'] = (request.user,)
   	        else:
   	            settings.UPDATED_DATA['INSPP']['PACKEDPRODUCT'] = ()
   	        return redirect('INSPPHome')


class PackedProductPackingMaterialView(DetailView):
   	model 		= PackedProductPackingMaterial

   	def get_context_data(self, **kwargs):
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')
   	    else:
   	        pppm=PackedProductPackingMaterial.objects.get(pk=self.kwargs['pk'])
   	        context = super(PackedProductPackingMaterialView, self).get_context_data(**kwargs)
   	        form =AddPackedProductPackingMaterialForm(instance=pppm)
   	        context['form'] = form
   	        return context
    
   	def post(self, request, *args, **kwargs):

   	    if 'edit' in request.POST:
   	        pppm=PackedProductPackingMaterial.objects.get(pk=self.kwargs['pk'])
   	        form = AddPackedProductPackingMaterialForm(request.POST, request.FILES , instance=pppm)			
   	        if form.is_valid():
   	            form.save()

   	            if request.COOKIES.get('app') !=None:
   	                settings.UPDATED_DATA['INSPP']['PACKEDPRODUCTPACKINGMATERIAL'] = (request.user,)
   	            else:
   	                settings.UPDATED_DATA['INSPP']['PACKEDPRODUCTPACKINGMATERIAL'] = ()
            

   	        return redirect('EditPackedProductPackingMaterial', pppm.pk)


   	    elif 'delete' in request.POST:
   	        pppm=PackedProductPackingMaterial.objects.get(pk=self.kwargs['pk'])
   	        pppm.delete()

   	        if request.COOKIES.get('app') !=None:
   	            settings.UPDATED_DATA['INSPP']['PACKEDPRODUCTPACKINGMATERIAL'] = (request.user,)
   	        else:
   	            settings.UPDATED_DATA['INSPP']['PACKEDPRODUCTPACKINGMATERIAL'] = ()
            
   	        return redirect('INSPPHome')


class OrderView(DetailView):
   	model 		= Order

   	def get_context_data(self, **kwargs):
   	    if not self.request.user.is_authenticated:
   	        return redirect('login')
   	    else:
   	        order=Order.objects.get(pk=self.kwargs['pk'])
   	        context = super(OrderView, self).get_context_data(**kwargs)
   	        form =AddOrderForm(instance=order)
   	        context['form'] = form
   	        return context
    
   	def post(self, request, *args, **kwargs):


   	    if 'edit' in request.POST:
   	        order=Order.objects.get(pk=self.kwargs['pk'])
   	        form = AddOrderForm(request.POST, request.FILES , instance=order)			
   	        if form.is_valid():
   	            form.save()
   	            if request.COOKIES.get('app') !=None:
   	                settings.UPDATED_DATA['INSPP']['ORDER'] = (request.user,)
   	            else:
   	                settings.UPDATED_DATA['INSPP']['ORDER'] = ()

   	        return redirect('EditOrder', order.pk)

   	    elif 'delete' in request.POST:
   	        order=Order.objects.get(pk=self.kwargs['pk'])
   	        order.delete()

   	        if request.COOKIES.get('app') !=None:
   	            settings.UPDATED_DATA['INSPP']['ORDER'] = (request.user,)
   	        else:
   	            settings.UPDATED_DATA['INSPP']['ORDER'] = ()

   	        return redirect('INSPPHome')


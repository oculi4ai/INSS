from INSPP.models import *
from users.models import *







@receiver(post_delete, sender=RawMaterial)
@receiver(post_delete, sender=RawMaterialsOutput)
@receiver(post_delete, sender=RawMaterialsInput)
@receiver(post_delete, sender=UnpackedProduct)
@receiver(post_delete, sender=UnpackedProductRawMaterial)
@receiver(post_delete, sender=PackedProduct)
@receiver(post_delete, sender=PackingMaterial)
@receiver(post_delete, sender=PackedProductPackingMaterial)
@receiver(post_delete, sender=PackingMaterialOutput)
@receiver(post_delete, sender=PackingMaterialInput)
@receiver(post_delete, sender=Order)
def delete_log(sender,instance, **kwargs):
    table = (type(sender()).__name__)
    
    add_log('DELETE',table,instance.pk,datetime.datetime.now().isoformat())



@receiver(post_save, sender=RawMaterial)
@receiver(post_save, sender=RawMaterialsOutput)
@receiver(post_save, sender=RawMaterialsInput)
@receiver(post_save, sender=UnpackedProduct)
@receiver(post_save, sender=UnpackedProductRawMaterial)
@receiver(post_save, sender=PackedProduct)
@receiver(post_save, sender=PackingMaterial)
@receiver(post_save, sender=PackedProductPackingMaterial)
@receiver(post_save, sender=PackingMaterialOutput)
@receiver(post_save, sender=PackingMaterialInput)
@receiver(post_save, sender=Order)
@receiver(post_save, sender=mail)
@receiver(post_save, sender=User)
def create(sender, instance, created, **kwargs):
    if sender == User:
        if created:
            print(instance.username_to)
            user = User.objects.get(username = instance.username)
            
            folder_id = Folder.objects.create(name = instance.username+'_storage' , owner = user ,privet = 0, MainFolder = None).id
            Profile.objects.create(user=instance,database_code='', storage_file_pk = folder_id)

    if sender == mail:
        
        if not created:
            if instance.pk not in json.loads(instance.username_from.profile.mail_edited):
                instance.username_from.profile.mail_edited = json.dumps(json.loads(instance.username_from.profile.mail_edited) + [instance.pk,])
                instance.username_from.profile.save()

            if instance.pk not in json.loads(instance.username_to.profile.mail_edited) :
                instance.username_to.profile.mail_edited = json.dumps(json.loads(instance.username_to.profile.mail_edited) + [instance.pk,])
                instance.username_to.profile.save()
        print('signal',created)

    if sender == RawMaterial:
        
        if created:
            values = json.dumps((instance.name,instance.m_type,instance.code,float(instance.quantity),instance.unit,float(instance.density),int(instance.loq_warning),float(instance.loq_quantity),instance.loq_unit))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','RawMaterial',values,date_and_time)
        else:
            values = json.dumps((instance.name,instance.m_type,instance.code,float(instance.quantity),instance.unit,float(instance.density),int(instance.loq_warning),float(instance.loq_quantity),instance.loq_unit,instance.pk))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('EDIT','RawMaterial',values,date_and_time)
    
    elif sender == RawMaterialsInput:
        if created:

            values = json.dumps((instance.material.id,int(instance.quantity),instance.unit,instance.date.isoformat(),instance.note))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','RawMaterialsInput',values,date_and_time)

            rm =RawMaterial.objects.get(pk = instance.material.id)
            quantity = float(rm.quantity) * material_units_convert[rm.unit] + float(instance.quantity) * material_units_convert[instance.unit]  
            quantity = convert_to_best_unit(quantity,base_unit[rm.unit][0],base_unit[rm.unit][1])
            rm.quantity = quantity[0]
            rm.unit = quantity[1]
            rm.save()

    elif sender == RawMaterialsOutput:
        if created:
            values = json.dumps((instance.material.id,int(instance.quantity),instance.unit,instance.date.isoformat(),instance.note))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','RawMaterialsOutput',values,date_and_time)

            rm =RawMaterial.objects.get(pk = instance.material.id)
            quantity = float(rm.quantity) * material_units_convert[rm.unit] - float(instance.quantity) * material_units_convert[instance.unit]  
            quantity = convert_to_best_unit(quantity,base_unit[rm.unit][0],base_unit[rm.unit][1])
            rm.quantity = quantity[0]
            rm.unit = quantity[1]
            rm.save()

    elif sender == UnpackedProductRawMaterial:
        
        if created:
            values = json.dumps((instance.product.id,instance.material.id,float(instance.percent)))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','UnpackedProductRawMaterial',values,date_and_time)
        else:
            values = json.dumps((instance.product.id,instance.material.id,float(instance.percent),instance.pk))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('EDIT','UnpackedProductRawMaterial',values,date_and_time)

    elif sender == PackingMaterial:

        if created:
            values = json.dumps((instance.name,instance.code,int(instance.quantity),instance.unit,int(instance.loq_warning) ,float(instance.loq_quantity)))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','PackingMaterial',values,date_and_time)
        else:
            values = json.dumps((instance.name,instance.code,int(instance.quantity),instance.unit,int(instance.loq_warning) ,float(instance.loq_quantity),instance.pk))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('EDIT','PackingMaterial',values,date_and_time)

    elif sender == PackingMaterialOutput:
        values = json.dumps((instance.material.id,str(instance.quantity),instance.date.isoformat() ,instance.note))
        date_and_time = datetime.datetime.now().isoformat()
        if created:
            add_log('CREATE','PackingMaterialOutput',values,date_and_time)
            pm =PackingMaterial.objects.get(pk = instance.material.id)
            quantity = pm.quantity - instance.quantity
            pm.quantity = quantity
            pm.save()
            
    elif sender == PackingMaterialInput:
        values = json.dumps((instance.material.id,str(instance.quantity),instance.date.isoformat() ,instance.note))
        date_and_time = datetime.datetime.now().isoformat()
        if created:
            add_log('CREATE','PackingMaterialInput',values,date_and_time)
            pm =PackingMaterial.objects.get(pk = instance.material.id)
            quantity = pm.quantity + instance.quantity#

            pm.quantity = quantity
            pm.save()

    elif sender == PackedProductPackingMaterial:
        
        if created:
            values = json.dumps((instance.packed_product.id,instance.packing_material.id,float(instance.count)))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','PackedProductPackingMaterial',values,date_and_time)
        else:
            values = json.dumps((instance.packed_product.id,instance.packing_material.id,float(instance.count),instance.pk))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('EDIT','PackedProductPackingMaterial',values,date_and_time)

    elif sender == UnpackedProduct:
        
        if created:
            values = json.dumps((instance.name,instance.code,instance.material_type,float(instance.quantity),instance.unit))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','UnpackedProduct',values,date_and_time)
        else:
            values = json.dumps((instance.name,instance.code,instance.material_type,float(instance.quantity),instance.unit,instance.pk))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('EDIT','UnpackedProduct',values,date_and_time)
        
    elif sender == PackedProduct:
        
        if created:
            values = json.dumps((instance.name,instance.code,instance.unpacked_product.id,float(instance.unpacked_product_quantity_in_one),instance.unit))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','PackedProduct',values,date_and_time)
        else:
            values = json.dumps((instance.name,instance.code,instance.unpacked_product.id,float(instance.unpacked_product_quantity_in_one),instance.unit,instance.pk))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('EDIT','PackedProduct',values,date_and_time)

    elif sender == Order:
        if created:
            values = json.dumps((instance.name,instance.code,instance.packed_product.id,float(instance.quantity),instance.starting_date.isoformat(),instance.planned_finishing_date.isoformat(),instance.actual_finishing_date.isoformat()))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('CREATE','Order',values,date_and_time)

            packed_product  = instance.packed_product
            for pm in packed_product.packedproductpackingmaterial_set.all():
                pm.packing_material.quantity = pm.packing_material.quantity - (instance.quantity * pm.count)
                pm.packing_material.save()

            for rm in packed_product.unpacked_product.unpackedproductrawmaterial_set.all():
                new_quantity = (float(rm.material.quantity) * float(material_units_convert[rm.material.unit]))- ( float(instance.quantity) * float(instance.packed_product.unpacked_product_quantity_in_one) * float(material_units_convert[instance.packed_product.unit]) * (float(rm.percent)/100) )
                new_quantity = convert_to_best_unit(new_quantity,base_unit[rm.material.unit][0],base_unit[rm.material.unit][1])
                rm.material.quantity    = new_quantity[0]
                rm.material.unit        = new_quantity[1]
                rm.material.save()

        else:
            values = json.dumps((instance.name,instance.code,instance.packed_product.id,float(instance.quantity),instance.starting_date.isoformat(),instance.planned_finishing_date.isoformat(),instance.actual_finishing_date.isoformat(),instance.pk))
            date_and_time = datetime.datetime.now().isoformat()
            add_log('EDIT','Order',values,date_and_time)
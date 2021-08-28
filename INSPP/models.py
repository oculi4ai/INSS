from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from decimal import Decimal
import datetime, json
from INSServer import settings




class RawMaterial(models.Model):
    material_types=[
        ('solid','solid'),
        ('liquid','liquid'),
        ('gas','gas')
    ]

    units=[
        ('solid',(
            ('MG','MG'),
            ('CG','CG'),
            ('DG','DG'),
            ('G','G'),
            ('DAG','DAG'),
            ('HG','HG'),
            ('KG','KG'),
            ('T','T'),
            )),
        ('Liquid / Gas',(
            ('ML','ML'),
            ('CL','CL'),
            ('DL','DL'),
            ('L','L'),
            ('DAL','DAL'),
            ('HL','HL'),
            ('KL','KL'))),

    ]

    name                = models.CharField(max_length=200, null=True, blank=True)
    m_type              = models.CharField(max_length=200,choices=material_types)
    code                = models.CharField(max_length=200, null=True, blank=True)
    quantity            = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    unit                = models.CharField(max_length=200,choices=units)
    density             = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    loq_warning         = models.BooleanField(default=0)
    loq_quantity        = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    loq_unit            = models.CharField(max_length=200,choices=units)
    

    def __str__(self):
        return self.name

class RawMaterialsOutput(models.Model):
    units=[
        ('solid',(
            ('MG','MG'),
            ('CG','CG'),
            ('DG','DG'),
            ('G','G'),
            ('DAG','DAG'),
            ('HG','HG'),
            ('KG','KG'),
            ('T','T'),
            )),
        ('Liquid / Gas',(
            ('ML','ML'),
            ('CL','CL'),
            ('DL','DL'),
            ('L','L'),
            ('DAL','DAL'),
            ('HL','HL'),
            ('KL','KL'))),

    ]
    material    = models.ForeignKey(RawMaterial, null=True, blank=True ,on_delete=models.CASCADE)
    quantity    = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    unit        = models.CharField(max_length=200,choices=units)
    date        = models.DateField()
    note        = models.TextField(null=True, blank=True)

class RawMaterialsInput(models.Model):
    units=[
        ('solid',(
            ('MG','MG'),
            ('CG','CG'),
            ('DG','DG'),
            ('G','G'),
            ('DAG','DAG'),
            ('HG','HG'),
            ('KG','KG'),
            ('T','T'),
            )),
        ('Liquid / Gas',(
            ('ML','ML'),
            ('CL','CL'),
            ('DL','DL'),
            ('L','L'),
            ('DAL','DAL'),
            ('HL','HL'),
            ('KL','KL'))),

    ]
    material    = models.ForeignKey(RawMaterial, null=True, blank=True ,on_delete=models.CASCADE)
    quantity    = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    unit        = models.CharField(max_length=200,choices=units)
    date        = models.DateField()
    note        = models.TextField(null=True, blank=True)

class UnpackedProduct(models.Model):
    material_types=[
        ('solid','solid'),
        ('liquid','liquid'),
        ('gas','gas')
    ]

    units=[
        ('Solid',(
            ('MG','MG'),
            ('CG','CG'),
            ('DG','DG'),
            ('G','G'),
            ('DAG','DAG'),
            ('HG','HG'),
            ('KG','KG'),
            ('T','T'),
            )),
        ('Liquid / Gas',(
            ('ML','ML'),
            ('CL','CL'),
            ('DL','DL'),
            ('L','L'),
            ('DAL','DAL'),
            ('HL','HL'),
            ('KL','KL'))),

    ]
    name                = models.CharField(max_length=200, null=True, blank=True)
    code                = models.CharField(max_length=200, null=True, blank=True)
    material_type       = models.CharField(max_length=200,choices=material_types)
    quantity            = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    unit                = models.CharField(max_length=200,choices=units, default=units[0])

    def __str__(self):
        return self.name

class UnpackedProductRawMaterial(models.Model):

    product                 = models.ForeignKey(UnpackedProduct, null=True, blank=True ,on_delete=models.CASCADE)
    material                = models.ForeignKey(RawMaterial, null=True, blank=True ,on_delete=models.CASCADE)
    percent                 = models.DecimalField(decimal_places=3,max_digits=100,default=0)

    def __str__(self):
        return self.product.name+' '+self.material.name

class PackedProduct(models.Model):
    units=[
        ('Solid',(
            ('MG','MG'),
            ('CG','CG'),
            ('DG','DG'),
            ('G','G'),
            ('DAG','DAG'),
            ('HG','HG'),
            ('KG','KG'),
            ('T','T'),
            )),
        ('Liquid / Gas',(
            ('ML','ML'),
            ('CL','CL'),
            ('DL','DL'),
            ('L','L'),
            ('DAL','DAL'),
            ('HL','HL'),
            ('KL','KL'))),

    ]
    name                                = models.CharField(max_length=200, null=True, blank=True)
    code                                = models.CharField(max_length=200, null=True, blank=True)
    unpacked_product                    = models.ForeignKey(UnpackedProduct, null=True, blank=True ,on_delete=models.CASCADE)
    unpacked_product_quantity_in_one    = models.DecimalField(decimal_places=3,max_digits=100,default=0)    
    unit                                = models.CharField(max_length=200,choices=units, default=units[0])

    def __str__(self):
        return self.name

class PackingMaterial(models.Model):
    units=[
        ('Piece','Piece'),
        ('Kilogram','Kilogram'),
        ('Metre','Metre'),
    ]

    name                = models.CharField(max_length=200, null=True, blank=True)
    code                = models.CharField(max_length=200, null=True, blank=True)
    quantity            = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    unit                = models.CharField(max_length=200,choices=units)
    loq_warning         = models.BooleanField(default=0)
    loq_quantity        = models.DecimalField(decimal_places=3,max_digits=100,default=0)

    def __str__(self):
        return self.name

class PackedProductPackingMaterial(models.Model):
    packed_product      = models.ForeignKey(PackedProduct, null=True, blank=True ,on_delete=models.CASCADE)
    packing_material    = models.ForeignKey(PackingMaterial, null=True, blank=True ,on_delete=models.CASCADE)
    count               = models.DecimalField(decimal_places=3,max_digits=100,default=0)


    def __str__(self):
        return self.packed_product.name+' '+self.packing_material.name

class PackingMaterialOutput(models.Model):

    material    = models.ForeignKey(PackingMaterial, null=True, blank=True ,on_delete=models.CASCADE)
    quantity    = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    date        = models.DateField()
    note        = models.TextField(null=True, blank=True)

class PackingMaterialInput(models.Model):
    material    = models.ForeignKey(PackingMaterial, null=True, blank=True ,on_delete=models.CASCADE)
    quantity    = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    date        = models.DateField()
    note        = models.TextField(null=True, blank=True)

class Order(models.Model):#'name','code','packed_product','quantity','starting_date','planned_finishing_date','actual_finishing_date','done'
    name                        = models.CharField(max_length=200, null=True, blank=True)
    code                        = models.CharField(max_length=200, null=True, blank=True)
    packed_product              = models.ForeignKey(PackedProduct, null=True, blank=True ,on_delete=models.CASCADE)
    quantity                    = models.DecimalField(decimal_places=3,max_digits=100,default=0)
    starting_date               = models.DateField()
    planned_finishing_date      = models.DateField()
    actual_finishing_date       = models.DateField(null=True, blank=True)
    done                        = models.BooleanField(default=0)


    def __str__(self):
        return self.name


class INSPP_logs(models.Model):
    
    operation       = models.CharField(max_length=200000000, default='[]')
    table           = models.CharField(max_length=200000000, default='[]')
    values          = models.CharField(max_length=200000000, default='[]')
    date_and_time   = models.CharField(max_length=200000000, default='[]')
    distribution    = models.CharField(max_length=200000000, default='[]') # json ids list


    def __str__(self):
        return ('['+self.operation +']      '+ self.table +'    '+ self.values)

material_units_convert={
    'MG'    :0.001
    ,'CG'   :0.01
    ,'DG'   :0.1
    ,'G'    :1
    ,'DAG'  :10
    ,'HG'   :100
    ,'KG'   :1000
    ,'T'    :1000000
    
    ,'ML'   :0.001
    ,'CL'   :0.01
    ,'DL'   :0.1
    ,'L'    :1
    ,'DAL'  :10
    ,'HL'   :100
    ,'KL'   :1000

}

base_unit={
    'MG'    :('G','Solid')
    ,'CG'   :('G','Solid')
    ,'DG'   :('G','Solid')
    ,'G'    :('G','Solid')
    ,'DAG'  :('G','Solid')
    ,'HG'   :('G','Solid')
    ,'KG'   :('G','Solid')
    ,'T'    :('G','Solid')
    
    ,'ML'   :('L','Liquid')
    ,'CL'   :('L','Liquid')
    ,'DL'   :('L','Liquid')
    ,'L'    :('L','Liquid')
    ,'DAL'  :('L','Liquid')
    ,'HL'   :('L','Liquid')
    ,'KL'   :('L','Liquid')
}

material_types={
    'solid' :['MG','CG','DG','G','DAG','HG','KG','T'],
    'liquid':['ML','CL','DL','L','DAL','HL','KL'],
    'gas'   :['ML','CL','DL','L','DAL','HL','KL'],
    }


def convert_to_best_unit(value,unit,m_type):
    units=material_types[m_type.lower()]
    while True :
        if float(value)>=10 and units.index(unit)<len(units)-1 and unit.upper()!='KG':
            value=value/10
            unit=units[units.index(unit)+1]
        elif float(value)>=1000 and units.index(unit)<len(units)-1 and unit.upper()=='KG':
            value=value/1000
            unit=units[units.index(unit)+1]
        else:
            break
    return (value,unit)




def add_log(operation,table,values,date_and_time):
    INSPP_logs.objects.create(operation= operation,table = table,values= values,date_and_time= date_and_time,distribution= '')




            
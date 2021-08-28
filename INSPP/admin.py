from django.contrib import admin
from .models import *


admin.site.register(UnpackedProduct)
admin.site.register(RawMaterial)
admin.site.register(UnpackedProductRawMaterial)
admin.site.register(PackedProduct)
admin.site.register(PackingMaterial)
admin.site.register(PackedProductPackingMaterial)
admin.site.register(Order)
admin.site.register(RawMaterialsOutput)
admin.site.register(RawMaterialsInput)
admin.site.register(PackingMaterialOutput)
admin.site.register(PackingMaterialInput)
admin.site.register(INSPP_logs)

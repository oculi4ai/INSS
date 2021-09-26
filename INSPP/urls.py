

from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [#add_distribution

    path('INSPPHome/'                               , INSPP_home                                , name='INSPPHome'                       ),
    path('INSPPGetData/'                            , INSPP_view_data                           , name='INSPPLogs'                       ),#INSPP_view_update
    path('INSPPGetUpdatedTable/'                    , INSPP_view_update                         , name='INSPP_view_update'               ),
    

    path('AddUnpackedProduct/'                      , AddUnpackedProduct                        , name='AddUnpackedProduct'              ),
    path('AddRawMaterial/'                          , AddRawMaterial                            , name='AddRawMaterial'                  ),
    path('AddRawMaterialInput/'                     , AddRawMaterialsInput                      , name='AddRawMaterialInput'             ),
    path('AddRawMaterialOutput/'                    , AddRawMaterialsOutput                     , name='AddRawMaterialOutput'            ),
    path('AddUnpackedProductRawMaterial/'           , AddUnpackedProductRawMaterial             , name='AddUnpackedProductRawMaterial'   ),
    path('AddPackedProduct/'                        , AddPackedProduct                          , name='AddPackedProduct'                ),
    path('AddPackingMaterial/'                      , AddPackingMaterial                        , name='AddPackingMaterial'              ),
    path('AddPackingMaterialInput/'                 , AddPackingMaterialInput                   , name='AddPackingMaterialInput'         ),
    path('AddPackingMaterialOutput/'                , AddPackingMaterialOutput                  , name='AddPackingMaterialOutput'        ),
    path('AddPackedProductPackingMaterial/'         , AddPackedProductPackingMaterial           , name='AddPackedProductPackingMaterial' ),
    path('AddOrder/'                                , AddOrder                                  , name='AddOrder'                        ),

    path('RawMaterial/<int:pk>/'                    , RawMaterialView.as_view()                 , name='EditRawMaterial'                 ),
    path('PackingMaterial/<int:pk>/'                , PackingMaterialView.as_view()             , name='EditPackingMaterial'             ),
    path('UnpackedProduct/<int:pk>/'                , UnpackedProductView.as_view()             , name='EditUnpackedProduct'             ),
    path('UnpackedProductRawMaterial/<int:pk>/'     , UnpackedProductRawMaterialView.as_view()  , name='EditUnpackedProductRawMaterial'  ),
    path('PackedProduct/<int:pk>/'                  , PackedProductView.as_view()               , name='EditPackedProduct'               ),
    path('PackedProductPackingMaterial/<int:pk>/'   , PackedProductPackingMaterialView.as_view(), name='EditPackedProductPackingMaterial'),
    path('Order/<int:pk>/'                          , OrderView.as_view()                       , name='EditOrder'                       ),

    path('RawMaterials/'                            , RawMaterialsView.as_view()                , name='RawMaterials'                    ),
    path('UnpackedProducts/'                        , UnpackedProductsView.as_view()            , name='UnpackedProducts'                ),
    path('PackedProducts/'                          , PackedProductsView.as_view()              , name='PackedProducts'                  ),
    path('PackingMaterials/'                        , PackingMaterialsView.as_view()            , name='PackingMaterials'                ),
    path('Orders/'                                  , OrdersView.as_view()                      , name='Orders'                          ),


    




]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static
#general urls
app_name = 'shop'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='summary'),   
    path('product/', views.ProductListView, name='product'),
    path('<str:parent_or_child>/<int:pk>', views.ProductListView, name='product_cat'),
    path('search/', views.search, name="search"), 
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-from-cart/<pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
]
if not settings.DEBUG:    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
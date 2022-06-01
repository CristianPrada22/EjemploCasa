from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static
#general urls
app_name = 'shop'
urlpatterns = [
    path('', views.CartView.as_view(), name='summary'),    
    path('product/', views.ProductListView.as_view(), name='product'),
    path('search/', views.search, name="search"), 
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-from-cart/<pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path("process/", views.PaymentCreateView.as_view(), name="process"),
    path("failure/", views.PaymentFailureView.as_view(), name="failure"),
    path("pending/", views.PaymentPendingView.as_view(), name="pending"),
    path("success/", views.PaymentSuccessView.as_view(), name="success"),
    path("webhook/", views.payment_webhook, name="webhook"),
]
if not settings.DEBUG:    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
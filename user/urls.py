from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import View
from . import views
from django.conf import settings
from django.conf.urls.static import static
#general urls
app_name = 'user'
urlpatterns = [
    path(route='login/', view=views.LoginView.as_view(),name='login'),
    path(route='logout/', view=views.LogoutView.as_view(), name='logout'),
    path(route='signup/', view=views.SignupView.as_view(), name='signup' ),
    path(route='me/profile/', view=views.UpdateProfileView.as_view(), name='update' ),
    path(route='<str:username>/', view=views.UserDetailView.as_view(), name='detail' ),
]

if not settings.DEBUG:    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
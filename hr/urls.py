from django.urls import path
from hr import views
from django.conf import settings
from django.conf.urls.static import static

#general urls
app_name = 'hr'

""" URLs used in the HR application. """
urlpatterns = [
    path('recruitment/', views.RecruitmentView.as_view(), name='recruitment'),
    path('jobDescription/', views.JobDescriptionView.as_view(), name='jobDescription'),
    path('approveRequest/', views.ApproveRequestView.as_view(), name='approveRequest'),
    path('requestList/', views.RequestListView.as_view(), name='requestList'),
]
if not settings.DEBUG:    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
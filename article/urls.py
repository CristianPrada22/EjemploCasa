from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [
    path('', views.ArticleListView, name='article-list'),
    path('<str:parent_or_child>/<int:pk>', views.ArticleListView, name='article-cat'),
    path('<id>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
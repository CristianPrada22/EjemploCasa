from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404

from article.models import Category, Article
# Create your views here.

def ArticleListView(request, parent_or_child=None, pk=None):
    categories = Category.objects.filter(parent=None)
    
    if parent_or_child is None:
        articles = Article.objects.all()
        paginator = Paginator(articles, 6)
            
    elif parent_or_child == 'child':
        sub_cat= Category.objects.get(pk=pk)
        articles= sub_cat.article_set.all()
        paginator = Paginator(articles, 6)
            
    elif parent_or_child == 'parent':
        articles= []
        sub_cats= Category.objects.get(pk=pk).children.all()

        for sub_cat in sub_cats:
            prds = sub_cat.article_set.all()
            articles += prds
        paginator = Paginator(articles, 6)
            
    else:
        articles = []        
          
    page = request.GET.get('page')
 
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles= paginator.page(paginator.num_pages)

    return render(
        request,
        'news_list.html',
        {'categories': categories, 'articles': articles, }
    )

class ArticleDetailView(generic.DetailView):
    model: Article
    template_name = 'news_detail.html'

    def get_object(self):
        return get_object_or_404(Article, id = self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['article'] = self.get_object()
        return context
    
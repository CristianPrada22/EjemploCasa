from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from parler.admin import TranslatableAdmin
from article.models import Category, Article 
# Register your models here.

admin.site.register(Category, MPTTModelAdmin)

@admin.register(Article)
class ArticleAdmin(TranslatableAdmin):
    fieldsets = (
        (None, {'fields': (
            'name',
            'category',
            'image', 
            'title', 
            'abstract', 
            'content',
            'notes',
            'links',
            'more_information',
            'contacts',
            'tags',
            'active',
            )}
        ),
    )
    readonly_fields = ('date_created', 'date_updated',)
    list_filter = ('active','category','date_updated')
    list_display = ('id','name','category','active','date_created','date_updated')
    search_fields = ('name','title','category',)
    
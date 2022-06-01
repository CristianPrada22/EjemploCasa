from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Product, OrderItem, Order, Category, SubCategory
# Register your models here.

#admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    pass

class SubcategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields': ('name',)
                }
            ),
    )
    list_display = ('name', 'parent')
    inlines = [SubcategoryInline,]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name')
    fieldsets = [
        (None, {'fields': ('name', 'parent', )}),
    ]

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
from django.contrib import admin
from nonrel_troca_app.models import *

admin.site.register(GenericItem)

class CategoriesInLine(admin.StackedInline):
	model = Category

class CategoryAdmin(admin.ModelAdmin):
	inlines = [CategoriesInLine, ]


admin.site.register(Category, CategoryAdmin)

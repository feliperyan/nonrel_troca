from django.contrib import admin
from nonrel_troca_app.models import *
from django_facebook.admin import FacebookProfileAdmin

admin.site.register(GenericItem)

class CategoriesInLine(admin.StackedInline):
	model = Category

class CategoryAdmin(admin.ModelAdmin):
	inlines = [CategoriesInLine, ]


admin.site.register(TrocaUserProfile, FacebookProfileAdmin)
admin.site.register(Category, CategoryAdmin)

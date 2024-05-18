from django.contrib import admin

# Register your models here.
from . models import category



class categoryAdmin(admin.ModelAdmin):
    list_display=('category_name','slug')
    prepopulated_fields={'slug':('category_name',)}
                  
admin.site.register(category,categoryAdmin)
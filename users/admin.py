from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.site_header = "chequeirs"

@admin.register(Agence)
class AgenceAdmin(ImportExportModelAdmin):
   search_fields = ['AGENCE']
   list_display = ('AGENCE','AGENCELIB','TXFRAIS','TXCOMMV','CLIMAX','CLIATTR','CLIENT','ADRNO',
                    'VILLE', 'CONNECTE','AGCPTA','AGCOUR','IMPRAVIS','IMPRETAT','IBATAVIS','IBATETAT',
                    'IMPRMATR','IBATMATR','SYS_CREATED_BY','SYS_UPDATED_DATE','SYS_UPDATED_BY',
                    'SYS_VERSION_NUMBER','SYS_CREATED_DATE','CLIAGP')


# Your import logic here, using agence_instance as needed
@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
   search_fields = ['CODE_RACINE']
   list_display = ('CODE_RACINE','CODE_AGENCE','NOM')

  
class UserAdminConfig(admin.ModelAdmin):
    model = UserAub
    search_fields = ('email','firstname','phone','lastname','post','image','username')
    list_filter = ('email','firstname','phone','lastname','post','image','username','is_active', 'is_staff',)
    ordering = ('firstname',)  # Update the ordering field here
    list_display = ('email','firstname','phone','lastname','post','image','username','is_superuser',
                    'is_active', 'is_staff','is_blocked','password',)
    fieldsets = (
        (None, {'fields': ('email','firstname','phone','lastname','post','image','username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','firstname','phone','lastname','post','image','username','is_active','is_staff','is_blocked')
            }
         ),
    )

admin.site.register(UserAub, UserAdminConfig)    
admin.site.register(Demchq)  

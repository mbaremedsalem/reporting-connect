from import_export import resources, fields
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django import forms

# Register your models here.
admin.site.site_header = "chequeirs"



class DemchqForm(forms.ModelForm):
    class Meta:
        model = DemChq
        fields = '__all__'

class DemchqResource(resources.ModelResource):
    class Meta:
        model = DemChq

@admin.register(DemChq)
class DemchqAdmin(ImportExportModelAdmin):
    resource_class = DemchqResource
    search_fields = ['CLIENT']



  
class UserAdminConfig(admin.ModelAdmin):
    model = UserAub
    search_fields = ('email','firstname','phone','lastname','post','username')
    list_filter = ('email','firstname','phone','lastname','post','username','is_active', 'is_staff',)
    ordering = ('firstname',)  # Update the ordering field here
    list_display = ('email','firstname','phone','lastname','post','username','is_superuser',
                    'is_active', 'is_staff','is_blocked','password',)
    fieldsets = (
        (None, {'fields': ('email','firstname','phone','lastname','post','username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','firstname','phone','lastname','post','username','is_active','is_staff','is_blocked')
            }
         ),
    )

admin.site.register(UserAub, UserAdminConfig)    

admin.site.register(Caissier)    

admin.site.register(ChefAgence) 

admin.site.register(UserProfile) 
# Your import logic here, using agence_instance as needed

class chequeResource(resources.ModelResource):
    class Meta:
        model = cheque

class chequeForm(forms.ModelForm):
    class Meta:
        model = cheque
        fields = '__all__'

@admin.register(cheque)
class chequeAdmin(ImportExportModelAdmin):
    resource_class = chequeResource
    search_fields = ['numero_de_compte']
    list_display = ('id','numero_de_compte' ,'code_agence' ,'Nbre_carnet' ,'Nbre_feuilles',  
                'code_transaction' ,'nom_client', 'adresse', 'Code_Devise' ,'code_bank' ,'code_pays' ,
                'numero_de_debut' 
                    )
    form = chequeForm
        # Rendre le champ 'id' éditable
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ('id','numero_de_compte' ,'code_agence' ,'Nbre_carnet' ,'Nbre_feuilles',  
                'code_transaction' ,'nom_client', 'adresse', 'Code_Devise' ,'code_bank' ,'code_pays' ,
                'numero_de_debut' 
                            )}),
    ]
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ('id','numero_de_compte' ,'code_agence' ,'Nbre_carnet' ,'Nbre_feuilles',  
                'code_transaction' ,'nom_client', 'adresse', 'Code_Devise' ,'code_bank' ,'code_pays' ,
                'numero_de_debut' 
                            )}),
    ]

class ArchiveResource(resources.ModelResource):
    class Meta:
        model = Archive

class archiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = '__all__'

@admin.register(Archive)
class ArchiveAdmin(ImportExportModelAdmin):
    resource_class =  ArchiveResource

    search_fields = ['numero_de_compte']
    list_display = ('id','numero_de_compte' ,'code_agence' ,'nbrchq' ,'nbre_feuiles',  
                'code_transaction' ,'nom_de_client', 'addresse', 'status' ,'code_bank' ,'code_pays' ,
                'numero_de_debut' 
                    )
    form = archiveForm
        # Rendre le champ 'id' éditable
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ('id','numero_de_compte' ,'code_agence' ,'nbrchq' ,'nbre_feuiles',  
                'code_transaction' ,'nom_de_client', 'addresse', 'status' ,'code_bank' ,'code_pays' ,
                'numero_de_debut' 
                            )}),
    ]
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ('id','numero_de_compte' ,'code_agence' ,'nbrchq' ,'nbre_feuiles',  
                'code_transaction' ,'nom_de_client', 'addresse', 'status' ,'code_bank' ,'code_pays' ,
                'numero_de_debut' 
                            )}),
    ]    
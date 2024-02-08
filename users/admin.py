from import_export import resources, fields
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django import forms

# Register your models here.
admin.site.site_header = "chequeirs"

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        fields = '__all__'

class AgenceResource(resources.ModelResource):
    class Meta:
        model = Agence

@admin.register(Agence)
class AgenceAdmin(ImportExportModelAdmin):
    resource_class = AgenceResource
    search_fields = ['AGENCE']
    list_display = ('id', 'AGENCE', 'AGENCELIB', 'TXFRAIS', 'TXCOMMV', 'CLIMAX', 'CLIATTR', 'CLIENT', 'ADRNO',
                    'VILLE', 'CONNECTE', 'AGCPTA', 'AGCOUR', 'IMPRAVIS', 'IMPRETAT', 'IBATAVIS', 'IBATETAT',
                    'IMPRMATR', 'IBATMATR', 'SYS_CREATED_BY', 'SYS_UPDATED_DATE', 'SYS_UPDATED_BY',
                    'SYS_VERSION_NUMBER', 'SYS_CREATED_DATE', 'CLIAGP')
    form = AgenceForm
        # Rendre le champ 'id' éditable
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ('id', 'AGENCE', 'AGENCELIB', 'TXFRAIS', 'TXCOMMV', 'CLIMAX', 'CLIATTR', 'CLIENT', 'ADRNO',
                            'VILLE', 'CONNECTE', 'AGCPTA', 'AGCOUR', 'IMPRAVIS', 'IMPRETAT', 'IBATAVIS', 'IBATETAT',
                            'IMPRMATR', 'IBATMATR', 'SYS_CREATED_BY', 'SYS_UPDATED_DATE', 'SYS_UPDATED_BY',
                            'SYS_VERSION_NUMBER', 'SYS_CREATED_DATE', 'CLIAGP')}),
    ]

class DemchqForm(forms.ModelForm):
    class Meta:
        model = Demchq
        fields = '__all__'

class DemchqResource(resources.ModelResource):
    class Meta:
        model = Demchq

@admin.register(Demchq)
class DemchqAdmin(ImportExportModelAdmin):
    resource_class = DemchqResource
    search_fields = ['CLIENT']
    list_display = ('id','CLIENT' ,'COMPTE' ,'DEVISE' ,'RESID', 'NCG', 
                'LIBELLE' ,'NBRCHQ', 'TYPCHQ', 'ADRL1' ,'ADRNAT' ,'ADRL2' ,
                'ADRNO' ,'ADRL3' ,'ADRL4' ,'ADRL5' ,'DATDEM' ,'DATEDDEM', 
                'DATREDEM' ,'DATREMCL' ,'DATMAJ' ,'REFER1' ,'REFER2' ,'NBRSOU' ,
                'CLERIB' ,'CHQREM' ,'CHQRES' ,'ADRL6','INSTR' ,'ANNUL' ,'DATDES' ,
                'CHQDET' ,'STATE' ,'VALIDE' ,'EXPL' ,'XCIRCUL' ,'XEXPED' ,'CORCLI' ,
                'CORADRNO' ,'NSERLOT' ,'DELAI' ,'NATDEM' ,'CREMDEM' ,'CREMEFF' ,
                'XAVIS' ,'XPRIOR' ,'XRENOUV' ,'XTOPE' ,'EXPLVALID','DATVALID' ,
                'NOOPER' ,'DADRNO' ,'DADRNAT','DADRL1' ,'DADRL2' ,'DADRL3' ,
                'DADRL4','DADRL5' ,'DADRL6' ,'CIRCULANT' ,'RENOUVNBR' ,'DATHDEM' ,
                'TYPRUE','TYPIMM1' ,'TYPIMM2' ,'CODPOST' ,'DCODPOST','DTYPRUE' ,
                'DTYPIMM1' ,'DTYPIMM2','DNUMRUE' ,'NUMRUE' ,
                    )
    form = DemchqForm
        # Rendre le champ 'id' éditable
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ('id','CLIENT' ,'COMPTE' ,'DEVISE' ,'RESID', 'NCG', 
                'LIBELLE' ,'NBRCHQ', 'TYPCHQ', 'ADRL1' ,'ADRNAT' ,'ADRL2' ,
                'ADRNO' ,'ADRL3' ,'ADRL4' ,'ADRL5' ,'DATDEM' ,'DATEDDEM', 
                'DATREDEM' ,'DATREMCL' ,'DATMAJ' ,'REFER1' ,'REFER2' ,'NBRSOU' ,
                'CLERIB' ,'CHQREM' ,'CHQRES' ,'ADRL6','INSTR' ,'ANNUL' ,'DATDES' ,
                'CHQDET' ,'STATE' ,'VALIDE' ,'EXPL' ,'XCIRCUL' ,'XEXPED' ,'CORCLI' ,
                'CORADRNO' ,'NSERLOT' ,'DELAI' ,'NATDEM' ,'CREMDEM' ,'CREMEFF' ,
                'XAVIS' ,'XPRIOR' ,'XRENOUV' ,'XTOPE' ,'EXPLVALID','DATVALID' ,
                'NOOPER' ,'DADRNO' ,'DADRNAT','DADRL1' ,'DADRL2' ,'DADRL3' ,
                'DADRL4','DADRL5' ,'DADRL6' ,'CIRCULANT' ,'RENOUVNBR' ,'DATHDEM' ,
                'TYPRUE','TYPIMM1' ,'TYPIMM2' ,'CODPOST' ,'DCODPOST','DTYPRUE' ,
                'DTYPIMM1' ,'DTYPIMM2','DNUMRUE' ,'NUMRUE' ,
                            )}),
    ]

# Your import logic here, using agence_instance as needed
@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
   readonly_fields = ('id',)
   search_fields = ['CODE_RACINE']
   list_display = ('id','CODE_RACINE','CODE_AGENCE','NOM')

  
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


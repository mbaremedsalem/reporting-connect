from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "Reporting"

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
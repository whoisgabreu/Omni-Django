from django.contrib import admin
from .models import Usuario
from .forms import UsuarioAdminForm

# Register your models here.
# admin.site.register(Usuario)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm

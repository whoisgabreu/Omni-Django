from django.db import models
from django.contrib.auth.hashers import check_password

# Create your models here.
class Usuario(models.Model):
    # Campos booleanos:
    admin = models.BooleanField(default=False, help_text="Usuário tem acesso de administrador?")
    manager = models.BooleanField(default=False, help_text="Usuário é gerente?")
    pode_postar = models.BooleanField(default=True, help_text="Usuário pode criar postagens?")

    nome = models.CharField(max_length=100)
    email = models.CharField(unique=True)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.nome
    
    def is_admin(self):
        return self.admin
    
    def is_manager(self):
        return self.manager
    
    def can_post(self):
        return self.pode_postar
    
    def check_senha(self, senha):
        return check_password(senha, self.senha)
    

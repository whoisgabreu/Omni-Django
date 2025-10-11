from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario

class UsuarioAdminForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    senha_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirme a senha")

    class Meta:
        model = Usuario
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_confirm = cleaned_data.get("senha_confirm")
        if senha != senha_confirm:
            raise forms.ValidationError("As senhas não coincidem!")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # criptografa a senha
        usuario.senha = make_password(self.cleaned_data["senha"])
        if commit:
            usuario.save()
        return usuario

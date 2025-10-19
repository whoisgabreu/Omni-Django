from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario

# Create your views here.
def login_page(request):
    erro = None
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        print(email)
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.check_senha(senha):
                # Autenticação bem-sucedida
                request.session['usuario_id'] = usuario.id # salva id do usuário na sessão
                request.session['nome'] = usuario.nome  
                return redirect("/home/")  # redireciona para a página privada
            else:
                erro = "Senha incorreta"
        except Usuario.DoesNotExist:
            erro = "Usuário não encontrado"
    
    return render(request, "login - v4.html", {"erro": erro})


# Logout
def logout_view(request):
    request.session.flush()  # limpa a sessão
    return redirect("/")

# Decorator para páginas privadas
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper

# Dashboard
@login_required
def dashboard(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    return render(request, "dashboard.html", {"usuario": usuario})


# home
@login_required
def home(request):
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    return render(request, "index.html", {"usuario": usuario})

# Atualizar senha
@login_required
def atualizar_senha(request):
    # Pega o usuário logado a partir da sessão
    usuario = Usuario.objects.get(id=request.session['usuario_id'])

    if request.method == "POST":
        senha_atual = request.POST.get("current-password")
        nova_senha = request.POST.get("new-password")
        confirmar_senha = request.POST.get("confirm-password")

        # Verifica se a senha atual está correta
        if not check_password(senha_atual, usuario.senha):
            messages.error(request, "Senha atual incorreta.")
            return render(request, "atualizar_senha.html", {"usuario": usuario})

        # Verifica se a nova senha bate com a confirmação
        if nova_senha != confirmar_senha:
            messages.error(request, "A nova senha e a confirmação não conferem.")
            return render(request, "atualizar_senha.html", {"usuario": usuario})

        # Atualiza a senha do usuário
        usuario.senha = make_password(nova_senha)
        usuario.save()

        messages.success(request, "Senha atualizada com sucesso!")
        return redirect("home")  # redireciona para a home após alterar a senha

    return render(request, "atualizar_senha.html", {"usuario": usuario})
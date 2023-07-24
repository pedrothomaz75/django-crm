from django.shortcuts import render, redirect

# imports de django.contrib.auth para login de usuários
from django.contrib.auth import authenticate, login, logout

# imports django.contrib messages para mensagens de sucesso no cadastro e login
from django.contrib import messages

def home(request):
    # Condição de check de loggin in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticação
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login efetuado com sucesso !")
            return redirect('home')
        else:
            messages.success(request, "Usuário e/ou senha incorretos, tente novamente")
            return redirect('home')
    else:
        return render(request, 'home.html', {})
    

# Função de logout de usuário
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout feito com sucesso !')
    return redirect('home')

# Função de cadastro de usuário
def register_user(request):
    return render(request ,'register.html', {})



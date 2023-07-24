from django.shortcuts import render, redirect

# imports de django.contrib.auth para login de usuários
from django.contrib.auth import authenticate, login, logout

# imports django.contrib messages para mensagens de sucesso no login
from django.contrib import messages

from . forms import SignUpForm, AddRecordForm

from .models import Record




def home(request):
    records = Record.objects.all()

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
        return render(request, 'home.html', {'records': records})
    

# Função de logout de usuário
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout feito com sucesso !')
    return redirect('home')

# Função de cadastro de usuário
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # Autenticacao e login 
            # Depois que o usuário for cadastrado, as labels vão ficar vázias
            username = form.cleaned_data['username']
            passoword = form.cleaned_data['password1']
            user = authenticate(username=username, passoword=passoword)
            messages.success(request, "Cadastro realizado com sucesso !")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request ,'register.html', {'form': form})
    return render(request ,'register.html', {'form': form})


# Criando a função de visualização única do usuário
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request ,'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "Você deve estar logado para poder acessar a página")
        return redirect('home')
    
# Criando função de deletar usuário
def delete_record(request, pk):
    if request.user.is_authenticated:
        deletar = Record.objects.get(id=pk)
        deletar.delete()
        messages.success(request, "Usuário deletado com sucesso !")
        return redirect('home')
    else:
        messages.success(request, "Você deve estar logado para poder acessar a página")
        return redirect('home')

# Criando função de adicionar usuário
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Cadastro realizado com sucesso !")
                return redirect('home')      
        return render(request ,'add_record.html', {'form': form})
    else:
        messages.success(request, "Você deve estar logado para poder acessar a página")
        return redirect('home') 
    

# Criando função de atualização de dados do usuário
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados atualizados com sucesso !")
            return redirect('home') 
        return render(request ,'update_record.html', {'form': form})
    else:
        messages.success(request, "Você deve estar logado para poder acessar a página")
        return redirect('home')
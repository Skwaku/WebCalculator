from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.paginator import (Paginator,
                                   EmptyPage,
                                   PageNotAnInteger)
from .forms import *
from .models import *


def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user_username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                username = User.objects.get(username=user_username)
                user = authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request, f"You are now logged in as {user_username}.")
                    return redirect('calculator')
                else:
                    messages.error(request, 'Incorrect username or password.')
                    return redirect('login')

            except User.DoesNotExist:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong. Please try again")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'calculator/login.html', {'form': form})


@login_required(login_url="/")
def user_logout(request):
    try:
        auth.logout(request)
        return redirect('login')
    except Exception as e:
        pass


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('calculator')

            except Exception as e:
                messages.error(request, 'An unexpected error occurred. Please try again.')
                return redirect('register')

    else:
        form = RegistrationForm()
    return render(request, 'calculator/register.html', {'form': form})



@login_required(login_url="/")
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    contex = {'user_form': user_form}
    return render(request, 'calculator/profile.html', contex)



@login_required(login_url="/")
def user_calculator(request):
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            expression = form.cleaned_data['expression']
            hist = form.save(commit=False)
            try:
                result = eval(str(expression))
                hist.user = request.user
                hist.expression = expression
                hist.result = result
                hist.save()
                data = {'result':result}
                return render(request, 'calculator/calculator.html', data)
            except ZeroDivisionError:
                hist.user = request.user
                hist.expression = expression
                hist.result = "Undefined: dividing by zero"
                hist.save()
                messages.error(request, 'Dividing by zero is undefined')
                return redirect('calculator')
            except Exception as e:
                messages.error(request, 'Invalid expression. Please try again.')
                return redirect('calculator')

    else:
        form = CalculatorForm()
    return render(request, 'calculator/calculator.html', {'form': form})



@login_required(login_url="/")
def user_history(request):
    history_list = History.objects.filter(user=request.user).order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(history_list, 10)
    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)

    return render(request, 'calculator/history.html', {'history': history})



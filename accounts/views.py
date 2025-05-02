
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.



def login_page(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.info(request,'Invalid Username! or User Do Not Exists')
            return redirect('SignIn')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.info(request,'Invalid Password!')
            return redirect('SignIn')
        else:
            login(request,user) 
            return redirect('/home')
    return render(request,'log.html')


from django.contrib.auth import get_user_model  # Import get_user_model
from django.core.exceptions import ValidationError

def sign_up(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('confirm_password')

        if c_password != password:
            messages.error(request, 'Passwords do not match.')
            return redirect('SignUp')

        User = get_user_model()

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('SignUp')

        try:
            user = User.objects.create_user( 
                username=username,
                email=email,
            )
            user.set_password(password)
            user.full_clean()  # Validate the user object before saving
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('SignIn')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}") #Show the user what went wrong
            return redirect('SignUp')
    return render(request, 'sig.html')


def logout_user(request):
    logout(request)
    messages.info(request,'You Have Been Logged Out.')
    return redirect('SignUp')
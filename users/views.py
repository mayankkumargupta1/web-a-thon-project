from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import logout
from .models import verify_code


from django.core.mail import send_mail
from website.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
import random
from django.contrib.sites.shortcuts import get_current_site

def send_test_email(user: str,subject: str, text: str, email: str) -> bool:
    message = render_to_string("email_format.html", {
        'user': user,
        'text' : text,
    })
    email = EmailMessage(subject, message, to=[email])
    if email.send():
        return True

    else:
        return False





from django.shortcuts import redirect


def user_not_authenticated(functions=None, redirect_urls='/'):
    """
    """
    def decorator(view_func):
        def _wrapped_view(request,*args,**kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_urls)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if functions:
        return decorator(functions)
    
    return decorator



@user_not_authenticated()
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Please click on the link sent on your email. To complete registration.')
            user.is_active = False
            user.save()
            random_number = random.randint(10000000, 99999999)
            
            username = user.username
            protocol = 'https' if request.is_secure() else 'http'
            domain = get_current_site(request).domain
            
            code = verify_code(user=user,code=random_number)
            code.save()
            send_test_email(user=username, subject='EMAIL VERFICATION', text=f'{protocol}://{domain}/user/verify/{random_number}', email=f'{user.email}')
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url='/user/login')
def custom_logout(request):
    logout(request)
    return redirect('/')

def verify_email(request, code):
    # login(request, user)
    code = verify_code.objects.filter(code=code)
    if code.exists():
        user = code.first().user
        user.is_active = True
        user.save()
        code.delete()
        return redirect('/')
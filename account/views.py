from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.views.generic import TemplateView, View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from account.tokens import account_activation_token
from account.forms import SignUpForm


class ProfileView(TemplateView):
    template_name = 'logged/profile.html'


class BeginView(TemplateView):
    template_name = 'begin.html'


class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form,
        }
        return render(request, 'registration/signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Expense Tracker Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account-activation-sent')
        else:
            context = {
                'form': form,
            }
            return render(request, 'registration/signup.html', context)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'registration/login.html', context)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.POST['username'])
            login(request, user)
            return redirect('home')
        else:
            context = {
                'form': form,
            }
            return render(request, 'registration/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ResetPasswordView(View):
    def get(self, request):
        form = PasswordResetForm()
        context = {
            'form': form,
        }
        return render(request, 'registration/reset_password.html', context)

    def post(self, request):
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=request.POST['email'])
            except User.DoesNotExist:
                error_msg = 'User with specified email does not exists.'
                context = {
                    'form': form,
                    'error': error_msg,
                }
                return render(request, 'registration/reset_password.html', context)
            else:
                form.save(domain_override='127.0.0.1:8000')
                return redirect('password-reset-sent')

        else:
            context = {
                'form': form,
            }
            return render(request, 'registration/reset_password.html', context)


def password_reset_sent(request):
    return render(request, 'registration/password_reset_sent.html')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'registration/account_activation_complete.html')
    else:
        return render(request, 'registration/account_activation_invalid.html')

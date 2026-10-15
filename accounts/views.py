from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'أهلاً فيك {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'اسم المستخدم أو كلمة السر غلط.')
        return super().form_invalid(form)


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'تم إنشاء حسابك بنجاح! أهلاً {user.first_name or user.username}')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'في خطأ بالتسجيل، تحقق من البيانات.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'تم تسجيل الخروج.')
    return redirect('core:home')


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    # تحديث حالة التحقق من الإيميل من allauth
    try:
        from allauth.account.models import EmailAddress
        email_address = EmailAddress.objects.get(user=request.user, email=request.user.email)
        profile_obj.email_verified = email_address.verified
        profile_obj.save()
    except Exception:
        pass

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(
            instance=profile_obj,
            initial={
                'first_name': request.user.first_name,
                'email': request.user.email,
            }
        )

    # طلبات المستخدم
    from requests_app.models import ProjectRequest
    user_requests = ProjectRequest.objects.filter(email=request.user.email).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile_obj,
        'user_requests': user_requests,
    })

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'تم إنشاء حسابك! أهلاً {user.first_name or user.username}')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'في خطأ بالتسجيل.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'أهلاً {user.first_name or user.username}!')
            return redirect('accounts:profile')
        messages.error(request, 'اسم المستخدم أو كلمة السر غلط.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'تم تسجيل الخروج.')
    return redirect('core:home')


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

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

    from requests_app.models import ProjectRequest
    user_requests = ProjectRequest.objects.filter(email=request.user.email).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile_obj,
        'user_requests': user_requests,
    })

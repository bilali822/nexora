from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def verify_email(request):
    messages.info(request, 'التوثيق قيد التطوير')
    return redirect('accounts:profile')


@login_required
def confirm_email(request, token):
    messages.info(request, 'التوثيق قيد التطوير')
    return redirect('accounts:profile')

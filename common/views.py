from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from account.models import User


def index(request):
    return render(request, 'common/index.html')


def unconfirmed_teachers(request):
    if not request.user.is_superuser:
        return redirect('/')
    token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'common/unconfirmed_teachers.html', {
        'unconfirmed_count': User.objects.filter(job=1, confirmed=False).count(),
        'unconfirmed_teachers': User.objects.filter(job=1, confirmed=False),
        'token': token.key
    })

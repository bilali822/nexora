"""Rate limiting مخصص بدون مكتبات خارجية"""
from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render


def ratelimit(key='ip', rate='5/h', block=True):
    """
    limit decorator
    key: 'ip' | 'user'
    rate: '5/h' | '10/m' | '100/d'
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            # احسب المفتاح
            if key == 'user' and request.user.is_authenticated:
                cache_key = f'ratelimit:{key}:{request.user.id}:{request.path}'
            else:
                ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
                ip = ip.split(',')[0].strip()
                cache_key = f'ratelimit:{key}:{ip}:{request.path}'

            # احسب الحد والوقت
            limit, period = rate.split('/')
            limit = int(limit)
            seconds = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}.get(period, 3600)

            # اقرأ العداد
            count = cache.get(cache_key, 0)
            if count >= limit:
                if block:
                    return render(request, '429.html', status=429)
                return view_func(request, *args, **kwargs)

            # زيادة العداد
            if count == 0:
                cache.set(cache_key, 1, seconds)
            else:
                cache.incr(cache_key)

            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

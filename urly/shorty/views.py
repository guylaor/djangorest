from django.shortcuts import render, redirect
from .models import ShortUrl
from rest_framework import viewsets
from .serializers import ShortUrlSerializer
from django.http import HttpResponse, JsonResponse
import string


class UrlsViewSet(viewsets.ModelViewSet):

    queryset = ShortUrl.objects.all().order_by('-created')
    serializer_class = ShortUrlSerializer


def index(request, short_url_id):

    try:
        u = ShortUrl.objects.get(short_url=short_url_id)
    except ShortUrl.DoesNotExist:
        json = "url key {} was not found".format(short_url_id)
        return JsonResponse({'response': json})

    # very simple user agent detection
    user_agent_str = request.META['HTTP_USER_AGENT'].lower()
    if any(x in user_agent_str for x in ('ipad', 'tablet')):
        user_agent = 'tablet'
    elif any(x in user_agent_str for x in ('iphone', 'android')):
        user_agent = 'mobile'
    else:
        user_agent = 'desktop'

    if user_agent == 'tablet' and u.tablet_url is not None:
        redirect_url = u.tablet_url
    elif user_agent == 'mobile' and u.mobile_url is not None:
        redirect_url = u.mobile_url
    else:
        redirect_url = u.default_url

    # updating redirect count
    u.redirect_count = u.redirect_count + 1
    u.save()

    return redirect(redirect_url)

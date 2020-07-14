
from django.contrib.gis.geoip2 import GeoIP2


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_timezone(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if not ip == '127.0.0.1':
        response = GeoIP2().city(ip)
        country = response.get('country_code')
        timezone = response.get('time_zone')
        country_name = response.get('country_name')
    else:
        timezone = "Asia/Kolkata"
    return timezone


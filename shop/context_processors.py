from django.conf import settings
from django.contrib.auth.decorators import login_required

def email_host_user(request):
    return {
        'email_host_user': settings.EMAIL_HOST_USER,
    }
    
def user_profile(request):
    return {
        'user_mobile_phone': settings.MOBILE_HOST_USER,
    }
    
def facebook_user(request):
    return {
        'facebook_user': settings.FACEBOOK_USER,
    }
    
def linkedin_user(request):
    return {
        'linkedin_user': settings.LINKEDIN_USER,
    }
    
def instagram_user(request):
    return {
        'instagram_user': settings.INSTAGRAM_USER,
    }
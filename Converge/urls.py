from django.contrib.gis import admin
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from register.views import UserRegisterView, UserVerifyView, resendOtpView

from notification.views import storeNotificationTokenView, unsetNotificationTokenView

schema_view = get_schema_view(
    openapi.Info(
        title="Converge API",
        default_version="v1",
        description="Welcome to Converge API Docs and testing platform!",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    # Swagger Views
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('api/register/', UserRegisterView.as_view(), name='register_user'),
    path('api/verifyemail/', UserVerifyView.as_view(), name='verify_user'),
    path('api/resend-otp/', resendOtpView, name='resend_OTP'),

    # Expo Notification Tokens
    path('api/expotoken/', storeNotificationTokenView, name='expo_token_post'),
    path('api/del-expotoken/', unsetNotificationTokenView, name='expo_token_del'),
    
    path('api/', include('rest_framework.urls')),
    path('api/', include('drf_social_oauth2.urls',namespace='drf')),

    # Reset Password 
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),


    path('api/', include('home.urls')),

    path('api/event/', include('event.urls')),
    
    path('api/chat/', include('chat.urls')),
]

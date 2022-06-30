"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('dss/', include('dss.urls', namespace='dss')),
    path('lowongan/', include('lowongan.urls', namespace='lowongan')),
    path('kriteria/', include('kriteria.urls', namespace='kriteria')),
    path('nilai/', include('nilai.urls', namespace='nilai')),
    
    path('', indexV, name='index'),
    path('registrasi/', registrasiV, name='registrasi'),
    path('login/', loginV, name='login1'),
    path('logout/', logoutV, name='logout1'),
    path('lowong-kerja/', lowong_kerjaV, name='lowong_kerja'),

    # path('account/', include('django.contrib.auth.urls')),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_ubah1.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_ubah2.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset1.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset2.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset3.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset4.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
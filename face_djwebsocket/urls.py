"""face_djwebsocket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path, include
from facerec import views as v
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.huanying, name='index'),
    path('users/', include('facerec.urls')),
    path('users/', include('django.contrib.auth.urls')),

    path('index/', v.index),
    path('index/caiji/', v.index1),
    path('index/jiance/', v.index2),
    path('index/shibie/', v.index3),
    path('echo', v.echo2),
    path('caiji', v.caiji),
    path('jiance', v.jiance),
    path('shibie', v.shibie),
]




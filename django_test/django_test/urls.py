"""django_test URL Configuration

The `urlpatterns` list routes URLs to subviews. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function subviews
    1. Add an import:  from my_app import subviews
    2. Add a URL to urlpatterns:  path('', subviews.home, name='home')
Class-based subviews
    1. Add an import:  from other_app.subviews import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hmdb.urls')),
]

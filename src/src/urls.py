"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin

from profiles import views as profiles_views
from core import views as core_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
     url(r'^$', profiles_views.home, name='home'),
     url(r'^search/', core_views.search,name='search'),
     url(r'^search_result/', core_views.search_result, name='search_result'),
     url(r'^analyse/$', core_views.analyse, name='analyse'),
    url(r'^view_record/', core_views.view_record, name='viewRec'),
     url(r'^accounts/', include('allauth.urls')),
     url(r'^import_db_criminal/$', core_views.import_db_criminal, name='import_db_criminal'),
    url(r'^import_db_criminal_img/$', core_views.import_db_criminal_img, name='import_db_criminal_img'),
     url(r'^import_db_detective/$', core_views.import_db_detective, name='import_db_detective'),
     url(r'^import_db_dependent/$', core_views.import_db_dependent, name='import_db_dependent'),
     url(r'^import_db_crime/$', core_views.import_db_crime, name='import_db_crime'),
     url(r'^import_db_case/$', core_views.import_db_case, name='import_db_case'),
    url(r'^import_db_assignedto/$', core_views.import_db_assignedto, name='import_db_assignedto'),
    url(r'^import_db_dependson/$', core_views.import_db_dependson, name='import_db_dependson'),
    url(r'^import_db_connectedto/$', core_views.import_db_connectedto, name='import_db_connectedto'),
    url(r'^entryFormx/', core_views.entry,name='entryForm'),
    url(r'^profile/$', profiles_views.userProfile, name='profile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

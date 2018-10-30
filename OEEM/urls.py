from django.conf.urls import include, url
from rest_framework import routers
from django.contrib import admin
from oeem import views

router = routers.DefaultRouter()
router.register(r'otview', views.OtViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'OEEM.views.home', name='home'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adminactions/', include('adminactions.urls')),
    #url(r'^', include('model_report.urls')),
]

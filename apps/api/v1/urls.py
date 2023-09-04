from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

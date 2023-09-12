from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.custom_user import CustomUserViewSet
from .views.clients import CreateClientApiView, ClientApiView


router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('auth/', include(router_v1.urls)),
    path('auth/clients/', CreateClientApiView.as_view(), name='create_client'),
    path('auth/clients/me/', ClientApiView.as_view(), name='client_profile'),
    path('auth/', include('djoser.urls.jwt')),
]

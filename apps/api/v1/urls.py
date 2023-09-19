from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.clients import CreateClientApiView, ClientApiView
from .views.psychologist import (ApproacheViewSet, CreatePsychologistView,
                                 InstituteViewSet, ThemeViewSet,
                                 PsychologistProfileView)
from .views.custom_user import CustomUserViewSet


router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')

router_v1_1 = DefaultRouter()
router_v1_1.register('themes', ThemeViewSet)
router_v1_1.register('approaches', ApproacheViewSet)
router_v1_1.register('institutes', InstituteViewSet)


urlpatterns = [
    path('auth/', include(router_v1.urls)),
    path('auth/clients/', CreateClientApiView.as_view(), name='create_client'),
    path('auth/clients/me/', ClientApiView.as_view(), name='client_profile'),
    path('auth/psychologists/',
         CreatePsychologistView.as_view(),
         name='create_psychologist'),
    path('auth/psychologists/me/',
         PsychologistProfileView.as_view(),
         name='profile_psychologist'),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_v1_1.urls)),
]

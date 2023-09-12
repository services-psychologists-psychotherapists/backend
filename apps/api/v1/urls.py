from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import psychologist as psycho
from .views.clients import CreateClientApiView, ClientApiView
from .views.custom_user import CustomUserViewSet


router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register(r'themes', psycho.ThemeViewSet)
router_v1.register(r'approaches', psycho.ApproacheViewSet)
router_v1.register(r'institutes', psycho.InstituteViewSet)


urlpatterns = [
    path('auth/', include(router_v1.urls)),
    path('auth/clients/', CreateClientApiView.as_view(), name='create_client'),
    path('auth/clients/me/', ClientApiView.as_view(), name='client_profile'),
    path('auth/psychologists/',
         psycho.CreatePsychologistView.as_view(),
         name='create_psychologist'),
    path('auth/', include('djoser.urls.jwt')),
]

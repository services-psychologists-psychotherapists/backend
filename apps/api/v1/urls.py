from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.clients import CreateClientView, ClientView
from .views.custom_user import CustomUserViewSet
from .views.psychologist import (ApproacheViewSet, CreatePsychologistView,
                                 InstituteViewSet, ThemeViewSet,
                                 PsychologistProfileView)
from .views.sessions import ListCreateSlotView, FreeSlotsView, DeleteSlotView


router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')

router_v1_1 = DefaultRouter()
router_v1_1.register('themes', ThemeViewSet)
router_v1_1.register('approaches', ApproacheViewSet)
router_v1_1.register('institutes', InstituteViewSet)


urlpatterns = [
    path('auth/', include(router_v1.urls)),
    # Личный кабинет клиента
    path('auth/clients/me/', ClientView.as_view(), name='client_profile'),
    path('auth/clients/', CreateClientView.as_view(), name='create_client'),
    # Личный кабинет психолога
    path('auth/psychologists/slots/<int:pk>/',
         DeleteSlotView.as_view(),
         name='delete_slot'),
    path('auth/psychologists/slots/',
         ListCreateSlotView.as_view(),
         name='psycho_slots'),

    path('auth/psychologists/',
         CreatePsychologistView.as_view(),
         name='create_psychologist'),
    path('auth/psychologists/me/',
         PsychologistProfileView.as_view(),
         name='profile_psychologist'),
    # Аутентификация
    path('auth/', include('djoser.urls.jwt')),
    # Запись на сессию
    path('psychologists/<uuid:psychologist_id>/free_slots/',
         FreeSlotsView.as_view(),
         name='free_slots'),

    path('', include(router_v1_1.urls)),
]

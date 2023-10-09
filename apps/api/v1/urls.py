from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.clients import ClientView, CreateClientView
from .views.custom_user import CustomUserViewSet
from .views.psychologist import (ApproacheViewSet, CreatePsychologistView,
                                 FreeSlotsView, InstituteViewSet,
                                 PsychoCardCatalogView, PsychoListCatalogView,
                                 PsychologistProfileView,
                                 ShortPsychoCardCatalogView, ThemeViewSet,
                                 UploadFileView)
from .views.sessions import (CancelSessionView, CreateSessionView,
                             DeleteSlotView, ListCreateSlotView)

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
         name='add_and_list_psycho_slots'),
    path('auth/psychologists/me/',
         PsychologistProfileView.as_view(),
         name='profile_psychologist'),
    path('auth/psychologists/',
         CreatePsychologistView.as_view(),
         name='create_psychologist'),
    # Аутентификация
    path('auth/', include('djoser.urls.jwt')),
    # Запись и отмена сессий
    path('sessions/', CreateSessionView.as_view(), name='create_session'),
    path('sessions/<int:pk>/',
         CancelSessionView.as_view(),
         name='cancel_session'),
    # Каталог психологов
    path('psychologists/<uuid:id>/short/',
         ShortPsychoCardCatalogView.as_view(),
         name='short_psycho_card'),
    path('psychologists/<uuid:id>/free_slots/',
         FreeSlotsView.as_view(),
         name='free_slots'),
    path('psychologists/<uuid:id>/',
         PsychoCardCatalogView.as_view(),
         name='psycho_card'),
    path('psychologists/', PsychoListCatalogView.as_view(), name='catalog'),
    # Вспомогательные поинты
    path('file/upload/', UploadFileView.as_view(), name='file_upload'),
    path('', include(router_v1_1.urls)),
]

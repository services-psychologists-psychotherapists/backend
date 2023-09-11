from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.clients import CreateClientApiView, ClientApiView
from .views.psychologist import CreatePsychologistView

router_v1 = DefaultRouter()


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/clients/', CreateClientApiView.as_view(), name='create_client'),
    path('auth/clients/me/', ClientApiView.as_view(), name='client_profile'),
    path('auth/psychologists/create/',
         CreatePsychologistView.as_view(),
         name='create_psychologist'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

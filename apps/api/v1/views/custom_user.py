from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils.timezone import now
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from djoser.permissions import CurrentUserOrAdmin
from djoser.compat import get_user_email
from djoser import utils
from djoser.serializers import (
    UserCreateSerializer,
    ActivationSerializer,
    SendEmailResetSerializer,
    PasswordResetConfirmSerializer,
    SetPasswordSerializer,
)
from drf_yasg.utils import swagger_auto_schema

from apps.api.v1.serializers.custom_user import CustomUserMeSerializer
from apps.core import email
from config import settings

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    token_generator = default_token_generator

    def permission_denied(self, request, **kwargs):
        if (
            settings.HIDE_USERS
            and request.user.is_authenticated
            and self.action in ["update", "partial_update", "list", "retrieve"]
        ):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_instance(self):
        return self.request.user

    @swagger_auto_schema(auto_schema=None)
    def perform_create(self, serializer, *args, **kwargs):
        pass

    @action(
        ["get"],
        detail=False,
        permission_classes=(CurrentUserOrAdmin,),
        serializer_class=CustomUserMeSerializer,
    )
    def me(self, request, *args, **kwargs):
        """Общая информация о пользователе для формирования ЛК."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        ["post"],
        detail=False,
        permission_classes=(AllowAny,),
        serializer_class=ActivationSerializer,
    )
    def activation(self, request, *args, **kwargs):
        """Активация пользователей - отправить uid + token"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            email.ConfirmationEmail(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ["post"],
        detail=False,
        permission_classes=(AllowAny,),
        serializer_class=SendEmailResetSerializer,
    )
    def resend_activation(self, request, *args, **kwargs):
        """Повторая отправка письма с ссылкой для активации."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if not settings.SEND_ACTIVATION_EMAIL or not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        context = {"user": user}
        to = [get_user_email(user)]
        email.ClientActivationEmail(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ["post"],
        detail=False,
        permission_classes=(CurrentUserOrAdmin,),
        serializer_class=SetPasswordSerializer,
    )
    def set_password(self, request, *args, **kwargs):
        """Установка пароля"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            email.PasswordChangedConfirmationEmail(self.request, context).send(
                to
            )

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ["post"],
        detail=False,
        permission_classes=(AllowAny,),
        serializer_class=SendEmailResetSerializer,
    )
    def reset_password(self, request, *args, **kwargs):
        """Сброс пароля - отправка письма с ссылкой для ввода нового пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            email.PasswordResetEmail(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ["post"],
        detail=False,
        permission_classes=(AllowAny,),
        serializer_class=PasswordResetConfirmSerializer,
    )
    def reset_password_confirm(self, request, *args, **kwargs):
        """Сброс пароля - отправить новый пароль."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.set_password(serializer.data["new_password"])

        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            email.PasswordChangedConfirmationEmail(self.request, context).send(
                to
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    # отключаем ручки create/list/retrieve/update/partial_update/destroy
    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        pass

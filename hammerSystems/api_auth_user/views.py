import string
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.sessions.models import Session

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404

from django.shortcuts import render, redirect

from django.urls import reverse, reverse_lazy

from django.views import View

from .models import Profile, Friends

from django.shortcuts import get_object_or_404

def auth_token_generate():
    """
    Функция генерации случайного 4х значного токена для демонстрации СМС кода, генерирует при каждой попытке
    верификации
    :return: token:string
    """
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=4
        )
    )


def invite_code_generate():
    """
    Функция генерации случайного 6х значного кода для реферального инвайта, создается единожды при регистрации
    пользователя
    :return: invite_code: string
    """
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )


class VerificationUser(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect(reverse("api_auth_user:profile_user"))
        return render(request, 'api_auth_user/verification-user.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        # "Получение номера телефона с POST запроса"
        telephone = request.POST['auth_phone_number']
        # "Добавление номера телефона в словарь сессии"
        request.session['telephone'] = telephone
        token = auth_token_generate()
        request.session['token'] = token
        user = User.objects.filter(username=telephone).first()
        # Проверка наличие пользователя в БД, если отсутствует, создаем, где добавляем уникальный инвайт код
        # на связанную таблицу OneToOne Profile, в качестве логина - телефон, пароля - токен
        if not user:
            invite_code = invite_code_generate()
            user = User.objects.create_user(username=telephone, password=token)
            Profile.objects.create(user=user, invite_code=invite_code)
            return redirect(reverse("api_auth_user:login_user"))
        user.set_password(token)
        user.save()
        # Если юзер есть в БД просто генерируем ему случайный пароль (ставим токен)
        return redirect(reverse("api_auth_user:login_user"))


class SignIn(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect(reverse("api_auth_user:profile_user"))
        elif not request.session:
            return redirect(reverse("api_auth_user:verification_user"))
        context = {
            'telephone': request.session.get('telephone'),
            'token': request.session.get('token'),
        }
        return render(request, 'api_auth_user/login-user.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        # Получаем в пост запросе введенный пользователем токен
        password = request.POST['password']
        # Получаем логин в виде телефона из сессии
        telephone = request.session.get('telephone')
        # Производим аутентификацию использую токен из VerificationUser (должен совпадать с токеном из реквеста)
        user = authenticate(request, username=telephone, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("api_auth_user:profile_user"))

        # Редирект при неверном токене
        return redirect(reverse("api_auth_user:login_user"))


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("api_auth_user:verification_user"))


class ProfileUser(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not self.request.user.is_authenticated:
            return redirect(reverse("api_auth_user:verification_user"))
        # Вывод профиля пользователя со всеми приглашенными.
        friends_list = Friends.objects.filter(invited=self.request.user).select_related('inviting')
        context = {
            'friends': friends_list
        }
        return render(request, 'api_auth_user/user-profile.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        invite_code = request.POST['invite_code']
        current_user = request.user

        if invite_code == current_user.profile.invite_code:
            # 404 при попытке ввода собственного реферального кода
            raise Http404()

        # 404 при попытке ввода несуществующего реферального кода
        invited_user_id = get_object_or_404(Profile, invite_code=invite_code)

        # Добавление в "друзья" текущего юзера и связанного с реферальным кодом юзера
        Friends.objects.create(
            inviting=request.user, invited_id=invited_user_id.user_id
        )
        # Обновление флага пользователя о том, что он использовал чужой код
        current_user.profile.was_invited = True
        current_user.profile.save()

        return redirect(reverse("api_auth_user:profile_user"))
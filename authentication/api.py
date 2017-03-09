from django.contrib.auth import authenticate, login, logout
from rest_framework import views
from django.shortcuts import redirect


class LoginView(views.APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"))

        if user is None or not user.is_active:
            return redirect('/api_keys/')

        login(request, user)
        return redirect('/api_keys/')


class LogoutView(views.APIView):
    def get(self, request):
        logout(request)
        return redirect('/api_keys/')

from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

class Login(TemplateView):
    template_name = 'login.html'
    def get(self,request,*args,**kwargs):
        username = request.session.get('username')
        login_status = request.session.get('login_status',False)
        template_dict = dict(
            login_status=login_status
        )
        return render(request,self.template_name,template_dict)
    def post(self,request,*args,**kwargs):
        template_dict = dict()
        username = request.POST.get('username')
        user_password = request.POST.get('password')
        user = authenticate(request, username=username, password=user_password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            request.session['login_status'] = True
            return redirect('/')
        else:
            message = '帳號密碼錯誤！'
            template_dict = dict(message=message)
        return render(request,self.template_name,template_dict)
    
class Logout(TemplateView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('/')
    

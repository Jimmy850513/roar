
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.shortcuts import render

class Index(TemplateView):
    template_name = 'index.html'
    def get(self,request,*args,**kwargs):
        template_dict = dict()
        return render(request,self.template_name,template_dict)
    
class Operation(APIView):
    def get(self,request,*args,**kwargs):
        return Response()
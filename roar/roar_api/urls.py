
from django.urls import path,include
from .Controller.operation import Operation
from .Controller.operation import Index
urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('operation/',Operation.as_view(),name='operation')
]

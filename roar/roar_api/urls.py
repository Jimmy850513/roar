
from django.urls import path,include
from .Controller.operation import Operation
from .Controller.operation import Index
from .Controller.user import Login,Logout
urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('operation/<str:UID>/',Operation.as_view(),name='operation'),
    path('login/',Login.as_view(),name='Login'),
    path('logout/',Logout.as_view(),name='Logout')
]

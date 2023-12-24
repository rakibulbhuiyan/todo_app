from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('',views.Tasklist.as_view(), name='tasklist'),
    path('taskdetail/<int:pk>/',views.TaskDetail.as_view(), name='taskdetail'),
    path('Taskupdate/<int:pk>/',views.TaskUpdate.as_view(), name='Taskupdate'),
    path('Taskdelete/<int:pk>/',views.TaskDelete.as_view(), name='Taskdelete'),
    path('taskcreate/',views.TaskCreate.as_view(), name='taskcreate'),

    path('login/', views.CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',views.CustomRegister.as_view(), name='register'),

]
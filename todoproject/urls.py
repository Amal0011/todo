"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path("todos/add/",views.TodoCreateView.as_view(),name="todo-add"),
    path("todos/all/",views.TodoListView.as_view(),name="todo-list"),
    path("todos/<int:pk>/tasknamedit/",views.TodoTasknameEditView.as_view(),name="todo-taskname"),
    path("todos/summary/", views.TodoSummaryView.as_view(), name="todo-summary"),
    path("todos/<int:pk>/",views.TodoDetailView.as_view(),name="todo-detail"),
    path("todos/<int:pk>/remove/",views.TodoDeleteView.as_view(),name="todo-delete"),
    path("todos/<int:pk>/change/",views.TodoEditView.as_view(),name="todo-edit"),
    path("todos/completed/",views.TodoCompletedView.as_view(),name="todo-completed"),
    path("",views.SignUpView.as_view(),name="register"),
    path("login/",views.SignInView.as_view(),name="signin"),
    path("logout/",views.signout_view,name="emp-signout")
    
]

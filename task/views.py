from django.shortcuts import render,redirect
from django.views.generic import View
from task.models import todo
from django import forms
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout


class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password1","password2"]

        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "last_name":forms.TextInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "email":forms.EmailInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "username":forms.TextInput(attrs={"class":"form-control btn btn-outline-success text-white"}),
            "password":forms.PasswordInput(attrs={"class":"form-control btn btn-outline-success text-white"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control btn btn-outline-danger text-white"}))
    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control btn btn-outline-danger text-white"}))

    
class SignUpView(View):
    def get(self,request,*args,**kw):
        form = RegistrationForm()
        return render(request,"reg.html",{"form":form})
    def post(self,request,*args,**kw):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"reg.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kw):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kw):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pd = form.cleaned_data.get("password")
            usr = authenticate(request,username=uname, password=pd)
            print(usr)
            if usr:
                login(request, usr)
            return redirect("todo-list")
        return render(request,"login.html",{"form":form})



class TodoForm(forms.Form):
    task_name = forms.CharField()
    # user = forms.CharField()


class TodoCreateView(View):
    def get(self,request,*args,**kw):
        form = TodoForm()
        return render(request,"add.html",{"form":form})
# Create your views here.
 
    def post(self,request,*args,**kw):
        form = TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo.objects.create(**form.cleaned_data, user = request.user)
            messages.success(request,"Task successfully created")
            return redirect("todo-list")
        messages.error(request,"error")
        return render(request,"add.html",{"form":form})

class TodoListView(View):
    def get(self,request,*args,**kw):
        qs = todo.objects.filter(status=False, user = request.user).order_by("-date")
        return render(request,"list.html",{"todos":qs})

class TodoDetailView(View):
    def get(self,request,*args,**kw):
        id = kw.get('pk')
        qs = todo.objects.get(id=id)
        return render(request,"detail.html", {"todo":qs})
    
class TodoDeleteView(View):
    def get(self,request,*args,**kw):
        id = kw.get("pk")
        todo.objects.get(id=id).delete()
        messages.success(request,"task deleted")
        return redirect("todo-list")

class TodoEditView(View):
    def get(self,request,*args,**kw):
        print(kw)
        id=kw.get('pk')
        todo.objects.filter(id=id).update(status=True)
        messages.success(request,"Moved to completed tasks")
        return redirect("todo-list")
    
class TodoTasknameEditView(View): 
    def get(self,request,*args,**kw):
        form = TodoForm()
        id = kw.get('pk')
        return render(request,"edittaskname.html",{"form":form, "id":id})
    
    def post(self,request,*args,**kw):
        form = TodoForm(request.POST)
        id = kw.get("pk")
        if form.is_valid():
            print(form.cleaned_data)
            todo.objects.filter(id = id).update(task_name = form.cleaned_data.get('task_name'))
            messages.success(request,"Task successfully updated")
            return redirect("todo-list")
        messages.error(request,"error")
        return render(request,"edittaskname.html",{"form":form})

    
class TodoCompletedView(View):
    def get(self,request,*args,**kw):
        qs = todo.objects.filter(status=True, user = request.user).order_by("-date")
        return render(request,"completed.html",{"todos":qs})

class TodoSummaryView(View):
    def get(self, request, *args, **kw):
        todo_completed = todo.objects.filter(status=True, user = request.user)
        todo_pend = todo.objects.filter(status=False, user = request.user)
        all = todo_completed.count() + todo_pend.count()
        completed_count = todo_completed.count()
        return render(request, "summary.html", {"completed":completed_count, "todo_all":all, "todo_pend":todo_pend, "todo_completed":todo_completed})

def signout_view(request, *args, **kw):
    logout(request)
    return redirect("signin")
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView,FormView
from .models import Task
from django.urls import reverse_lazy 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class CustomLogin(LoginView):
    template_name='login.html'
    fields='__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('login')

class CustomRegister(FormView):
    template_name='register.html'
    form_class= UserCreationForm
    redirect_authenticated_user=True
    success_url= reverse_lazy('login')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(CustomRegister, self).get(*args,**kwargs)


class Tasklist(LoginRequiredMixin,ListView):
    model=Task
    template_name='task_list.html'
    context_object_name='tasks'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(complete=False).count()

        search_input=self.request.GET.get('search_value') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__icontains=search_input)
        context['search_input']=search_input
        return context



class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    template_name='task_detail.html'
    context_object_name='tasks'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    template_name='task_form.html'
    success_url=reverse_lazy('tasklist')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    template_name='task_form.html'
    success_url=reverse_lazy('tasklist')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    template_name='task_delete.html'
    success_url=reverse_lazy('tasklist')
    context_object_name='tasks'
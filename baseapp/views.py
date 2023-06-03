from django.shortcuts import render
from .models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    model=Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['taskDetail'] = Task.objects.filter(id=self.object.id)
        return context


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title","description"]
    success_url=reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The task was created successfully.")
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ["title","description"]
    template_name_suffix = "_update"
    success_url=reverse_lazy('task_list')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    success_url=reverse_lazy('task_list')
    
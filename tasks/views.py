from django.shortcuts import render
from django.urls import reverse_lazy
from tasks import models, forms
from django.views.generic import ListView, DetailView, CreateView

class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task_details.html"

class TaskCreateView(CreateView):
    models = models.Task
    template_name = "tasks/task_form.html"
    form_class = forms.TaskForm
    success_url = reverse_lazy("tasks:task-list")
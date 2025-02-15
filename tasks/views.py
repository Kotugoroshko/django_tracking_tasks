from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy, reverse
from tasks import models, forms, mixins
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login



class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status = status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.TaskFilterForm(self.request.GET)
        return context
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm()  # Додаємо порожню форму коментаря в контекст
        return context

    def post(self, request, *args, **kwargs):
            form = forms.CommentForm(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.task = self.get_object()
                comment.save()
                return redirect('tasks:task-details', pk=comment.task.pk)
            else:
                messages.error(request, "fields are not filled in!")
                return redirect("tasks:task-list")

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)
class TaskCreateView(LoginRequiredMixin, CreateView):
    models = models.Task
    template_name = "tasks/task_form.html"
    form_class = forms.TaskForm
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

class TaskCompleteView(LoginRequiredMixin, mixins.UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))
    
    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)
    
class TaskUpdateView(LoginRequiredMixin, mixins.UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = "tasks/task_update_form.html"
    success_url = reverse_lazy("tasks:task-list")

class TaskDeleteView(LoginRequiredMixin, mixins.UserIsOwnerMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "tasks/task_delete_confirmation.html"
    
class CommentEditView(LoginRequiredMixin, UpdateView):
    model = models.Comment
    template_name="tasks/edit_comment.html"
    fields = ["content"]

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Ви не можете редагувати цей коментар.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tasks:task-details', kwargs={'pk': self.object.task.pk})
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Comment
    template_name = "tasks/delete_comment.html"

    def get_success_url(self):
        return reverse_lazy('tasks:task-details', kwargs={'pk': self.object.task.pk})
    
    def get_queryset(self):
        queryset = super().get_queryset()
        comment_id = self.kwargs.get("pk")
        return queryset.filter(id = comment_id)
    
class CommentLikesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
        likes = models.Like.objects.filter(comment=comment, user=request.user)
        if likes.exists():
            likes.delete()
        else:
            models.Like.objects.create(comment=comment, user=request.user)
        return redirect('tasks:task-details', pk=comment.task.pk)

class CustomLoginView(LoginView):
    template_name = "tasks/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'tasks:login'


class RegisterView(CreateView):
    template_name = "tasks/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("tasks:login"))
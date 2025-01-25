from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Task(models.Model):

    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]
    PRIORITY_CHOICES = [
        ("low", "Low Priority"),
        ("medium", "Medium Priority"),
        ("high", "High Priority"),
    ]

    title = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True) #Null в базі даних, blank - користувач на сайті можене заповнити
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    
    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('tasks:task-details', kwargs={'pk': self.pk})

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return (f'{self.task.title} \n {self.author} - {self.content}')

    # def get_absolute_url(self):
    #     return self.get_absolute_url()
    
class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('comment', 'user')  # Забезпечує унікальність лайків
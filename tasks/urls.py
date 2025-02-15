from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.TaskListView.as_view(),name="task-list"),
    path('<int:pk>/', views.TaskDetailView.as_view(),name="task-details"),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(),name="task-update"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(),name="task-delete"),
    path('task-create', views.TaskCreateView.as_view(), name = "task-create"),
    path('<int:pk>/complete', views.TaskCompleteView.as_view(), name = "task-complete"),
    path('comment/edit/<int:pk>/', views.CommentEditView.as_view(), name='edit-comment'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('comment/like/<int:pk>/', views.CommentLikesView.as_view(), name='like-comment'),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
app_name = "tasks"


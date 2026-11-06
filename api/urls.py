from django.urls import path
from api import views

urlpatterns = [
    path('todos/', views.TodoListCreate.as_view()),
    # 新增下面这行，<int:pk> 代表接收一个数字ID
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()), 
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()),
    path('signup/', views.signup), # <--- 新增这行
]
from django.urls import path
from api import views

urlpatterns = [
    path('todos/', views.TodoListCreate.as_view()),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()),
    path('signup/', views.signup),
    path('login/', views.login),  # <--- 新增这行
]
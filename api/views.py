# 在文件最顶部的 import 区域加上这行
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, permissions
from api.serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo

# 引入注册需要的模块
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 1. 列表与创建视图
class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 2. 详情、更新与删除视图
class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

# 3. 切换完成状态视图
class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        # 将 completed 状态取反
        serializer.instance.completed = not(serializer.instance.completed)
        serializer.save()

# ==========================================
# 下面这两个函数，一个是注册，一个是登录，千万别搞混了
# ==========================================

# 4. 用户注册视图 (Signup)
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'username taken. choose another username'}, status=400)
            
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

# 5. 用户登录视图 (Login)
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
            request,
            username=data['username'],
            password=data['password']
        )
        if user is None:
            return JsonResponse({'error': 'unable to login. check username and password'}, status=400)
        else: 
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist: 
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
            
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
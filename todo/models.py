from django.contrib.auth.models import User
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # 自动记录创建时间
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 关联用户

    def __str__(self):
        return self.title
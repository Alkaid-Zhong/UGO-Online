from django.db import models


class Message(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)




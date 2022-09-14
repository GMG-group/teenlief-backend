from django.db import models


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    helper = models.ForeignKey(null=False, blank=False, on_delete=models.CASCADE, to='accounts.User', related_name='sender_helper')
    teen = models.ForeignKey(null=False, blank=False, on_delete=models.CASCADE, to='accounts.User', related_name='sender_teen')

    def __str__(self):
        return self.room_name


class ChatLog(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(null=False, blank=False, on_delete=models.CASCADE, to='accounts.User', related_name='user')

    def __str__(self):
        return self.content

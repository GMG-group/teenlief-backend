from django.db import models


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user1 = models.IntegerField(null=False, blank=False)
    user2 = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.room_name


class ChatLog(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.content

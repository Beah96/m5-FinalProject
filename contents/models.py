from django.db import models
import uuid

class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    content = models.TextField()
    video_url = models.CharField(max_length=200, null=True)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE, 
        related_name='contents'
    )

    



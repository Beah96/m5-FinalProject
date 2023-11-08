from django.db import models
import uuid

class Course_Status(models.TextChoices):
    NOT_STARTED = 'not started'
    IN_PROGRESS = 'in progress'
    FINISHED = 'finished'


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=11, 
        choices=Course_Status.choices,
        default=Course_Status.NOT_STARTED
    )
    start_date = models.DateField()
    end_date = models.DateField()
    
    instructor = models.ForeignKey(
        'accounts.Account', 
        on_delete=models.PROTECT,
        related_name='courses',
        null=True,
        default=None
    )
    students = models.ManyToManyField(
        'accounts.Account',
        through='students_courses.StudentCourse',
        related_name='my_courses'
    )
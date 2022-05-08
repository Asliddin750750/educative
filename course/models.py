from django.db import models
from account.models import User
from config.validators import VideoValidator


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Course(models.Model):
    DIFFICULTIES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        ('Expert', 'Expert')
    )

    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    teacher = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='teacher', limit_choices_to={
        'job': 1
    })
    students = models.ManyToManyField(User, related_name='students', limit_choices_to={
        'job': 2
    })
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='course/thumbnails/')
    intro_video = models.FileField(upload_to='course/intro_videos/', validators=[VideoValidator()])
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
        'job': 2
    })
    stars = models.PositiveSmallIntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    section = models.ForeignKey(Section, related_name='section', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    video = models.FileField(upload_to='lesson/', validators=[VideoValidator()])
    duration = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

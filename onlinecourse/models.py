from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=30, null=False, default='online course')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=200, default="lesson")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_courses = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'db_admin'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT,
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username

class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODE_CHOICES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'Beta')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now=True)
    mode = models.CharField(
        max_length=5,
        choices=COURSE_MODE_CHOICES,
        default=AUDIT
    )

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=5)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission ID: {self.id}"
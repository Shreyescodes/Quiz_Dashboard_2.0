from django.db import models
from django.contrib.auth.models import User

class QuizType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class QuizQuestion(models.Model):
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE, null=True)  # Keep it nullable for now
    question = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.quiz_type.name if self.quiz_type else 'No Type'} - {self.question[:50]}"

class QuizAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')])
    request_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz_type')

    def __str__(self):
        return f"{self.user.username} - {self.quiz_type.name} - {self.status}"

class QuizRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied')
    ], default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz_type.name} ({self.status})"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_attempted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz_type.name} (Score: {self.score})"

class QuizFile(models.Model):
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='quiz_files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quiz_type.name} - {self.file.name}"
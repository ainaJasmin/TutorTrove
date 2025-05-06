from django.db import models
from django.contrib.auth.models import User

class Tutor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email =  models.CharField(max_length=100)
    joined = models.DateTimeField(auto_now_add=True)
    phone =  models.IntegerField(null=True)
    hours =  models.IntegerField(null=True)
    approach = models.TextField(max_length=100, null=True)
    user_pic = models.ImageField(default="defaultProfilePic.jpeg", null=True, blank=True)

    def __str__(self):
        return self.name
    

class Level(models.Model):
    level_name = models.CharField(max_length=100, null=True)
    level_class = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.level_name
    
    
class Subject(models.Model):
    subject_name = models.CharField(max_length=100, null=True)
    exam_prep = models.BooleanField(null=True)
    price = models.FloatField(max_length=100, null=True)
    level = models.ForeignKey(Level, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.level} - {self.subject_name}"


class TutorSubject(models.Model):
    tutor = models.ForeignKey(Tutor, null=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    desc = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.tutor} ({self.subject})"


class Tutee(models.Model):
    name = models.CharField(max_length=100)
    tutor_subject = models.ManyToManyField(TutorSubject)
    joined = models.DateTimeField(auto_now_add=True)
    phone = models.IntegerField(null=True)
    level = models.ForeignKey(Level, null=True, on_delete=models.SET_NULL)

    def __str__(self):
       return self.name
    
class TuteeHours(models.Model):
    name = models.ForeignKey(Tutee, on_delete=models.CASCADE)
    hours = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.hours}hrs)"
    

class PaymentStatus(models.Model):
    PAYMENT_CHOICES = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    )
    tutor_subject = models.ForeignKey(TutorSubject, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Not Paid')
    month = models.DateField() 
    
    def __str__(self):
        return f"{self.tutor_subject} - {self.status} - {self.month.strftime('%b %Y')}"
        
    class Meta:
        unique_together = ('tutor_subject', 'month')
    

    
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    office = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    start_date = models.DateField()
    salary = models.PositiveIntegerField()

    def __str__(self):
        return self.name



# class Notification(models.Model):
#     text = models.CharField(max_length=200)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     sent = models.BooleanField(default=False)
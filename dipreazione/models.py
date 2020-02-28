from django.db import models

class Meater(models.Model):
    name = models.CharField(max_length=200)

class Meating(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()

class Preference(models.Model):
    meating = models.ForeignKey(Meating, on_delete=models.CASCADE)
    meater = models.ForeignKey(Meater, on_delete=models.CASCADE)
    date = models.DateField()


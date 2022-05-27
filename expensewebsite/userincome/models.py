from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User


class UserIncome(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.ForeignKey('Source', related_name='source', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.source}"

    def get_absolute_url(self):
        return reverse('income-edit', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

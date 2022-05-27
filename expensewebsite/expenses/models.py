from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='expense', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('expense-edit', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.category}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



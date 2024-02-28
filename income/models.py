from django.db import models
from django.contrib.auth.models import User

SOURCE_CHOICES = (
    ('0', 'Lương'),
    ('1', 'Kinh Doanh'),
    ('2', 'Phụ Thu Nhập'),
    ('3', 'Khác'),
)


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.user.username

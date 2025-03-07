from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Peca(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    code = models.CharField(max_length=120, unique=True)
    amount = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'

    def __str__(self):
        return self.name

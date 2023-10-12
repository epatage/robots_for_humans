from django.db import models
from django.db.models import CheckConstraint, Q


class RobotModel(models.Model):
    name = models.CharField(max_length=2, blank=False, null=False)


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(
        max_length=2,
        blank=False,
        null=False,
    )
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    sold = models.BooleanField(default=False)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(model__in=list(
                    RobotModel.objects.all().values_list('name', flat=True)
                )),
                name='Проверка модели робота',
            ),
        ]

    def __str__(self):
        return self.serial

from django.core.exceptions import ValidationError
from django.db import models


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

    def __str__(self):
        return self.serial

    def clean(self):
        robot_models = list(
            RobotModel.objects.all().values_list('name', flat=True)
        )

        if self.model not in robot_models:
            raise ValidationError(
                'Указана не существующая модель',
            )

from django.core.exceptions import ValidationError
from django.db import models


def validate_robot_model(value):
    """Проверяет соответствие модели робота с существующими в системе"""

    robot_models = list(
        RobotModel.objects.all().values_list('name', flat=True)
    )

    if value not in robot_models:
        raise ValidationError(
            'Указана не существующая модель',
        )


class RobotModel(models.Model):
    name = models.CharField(max_length=2, blank=False, null=False)


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        validators=[validate_robot_model],
    )
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

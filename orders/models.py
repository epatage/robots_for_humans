from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import Customer
from robots.models import Robot


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    purchase = models.ForeignKey(
        Robot,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


@receiver(post_save, sender=Robot)
def robot_created_signal(sender, instance, created, **kwargs):
    """
    Сигнал при изготовлении нового робота проверяет наличие заказа на данную
    серию и, в случае наличия ожидающего заказа,
    отправляет электронное письмо покупателю.
    """

    if created:
        robot = instance.serial
        model, version = robot.split('-')

        orders = Order.objects.filter(purchase=None, robot_serial=robot)

        if orders:
            order = orders[0]
            email = order.customer.email

            text_mail = \
                'Добрый день!\n'\
                f'Недавно вы интересовались нашим роботом модели {model}, '\
                f'версии {version}.\n'\
                'Этот робот теперь в наличии. Если вам подходит этот вариант - '\
                'пожалуйста, свяжитесь с нами.'

            send_mail(
                'Ваш робот готов!',
                f'{text_mail}',
                'robots@r4c.com',
                [f'{email}'],
            )

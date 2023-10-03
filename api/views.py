import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from robots.models import Robot
from django.db.utils import IntegrityError


@method_decorator(csrf_exempt, name='dispatch')
class RobotView(View):

    def get(self, request):

        robots = Robot.objects.all()
        robots_serialized_data = []

        for robot in robots:
            robots_serialized_data.append({
                'serial': robot.serial,
                'model': robot.model,
                'version': robot.version,
                'created': robot.created,
            })

        data = {
            'robots': robots_serialized_data,
        }
        return JsonResponse(data)

    def post(self, request):

        robot_data = json.load(request)

        robot = Robot()
        robot.model = robot_data.get('model')
        robot.version = robot_data.get('version')
        robot.created = robot_data.get('created')
        robot.serial = f'{robot.model}-{robot.version}'

        try:
            robot.full_clean()
            robot.save()

            # Для полного вывода информации при создании объекта
            robot_data['serial'] = robot.serial

        except IntegrityError as error:
            empty_value = str(error).rsplit('.')
            message = f'Не заполнено поле {empty_value[1]}'
            return JsonResponse({'message': message}, status=400)
        except ValidationError as error:
            message = f'Ошибка валидации: {error}'
            return JsonResponse({'message': message}, status=400)

        return JsonResponse(robot_data, status=201)

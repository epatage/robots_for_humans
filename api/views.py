import json

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook

from robots.models import Robot, RobotModel
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models import Count
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.borders import Border, Side


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


class TableCreatedRobots(View):
    """
    Выгрузка отчета по показателям производства роботов в Excel-таблицу.
    """

    # Период (количество дней) за который берутся данные в отчет
    report_days = 7

    # Заголовки колонок таблицы
    headers = ['Модель', 'Версия', 'Количество за неделю']

    # Параметры форматирования таблицы
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin'),
    )
    alignment = Alignment(horizontal="center")

    def get(self, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="created_robots.xlsx"'

        wb = Workbook()

        # Выборка всех моделей роботов (соответствует количеству листов)
        models = RobotModel.objects.all()

        # Переименование первого листа под первую модель робота
        ws = wb.active
        ws.title = models[0].name

        # Создание листов под каждую модель (начиная со второй)
        for model in models[1:]:
            wb.create_sheet(f'{model.name}')

        # Вычисление дат для периода запроса данных о производстве
        date_to = datetime.today()
        date_from = date_to - timedelta(days=self.report_days)

        # Выборка данных о производстве роботов за определенный период
        robots = Robot.objects.filter(created__range=(date_from, date_to))

        for model in models:
            # Переключение на лист текущей модели роботов
            ws = wb[model.name]

            # Создание промежуточной таблицы (словаря) с данными
            # версии робота и их количестве
            current_robots_model = robots.filter(
                model=model.name
            ).values('version').annotate(count=Count('version'))

            # Заполнение заголовков таблицы
            for col, val in enumerate(self.headers, start=1):
                cell = ws.cell(row=1, column=col, value=val)
                cell.alignment = self.alignment
                cell.border = self.border
                # Ширина колонок форматируется под ширину заголовков таблицы
                ws.column_dimensions[cell.column_letter].width = len(val) + 2

            # Заполнение таблицы
            row = 2
            for robot in current_robots_model:
                lst = [model.name, robot.get('version'), robot.get('count')]
                for col, val in enumerate(lst, start=1):
                    cell = ws.cell(row=row, column=col, value=val)
                    cell.alignment = self.alignment
                    cell.border = self.border
                row += 1

        wb.save(response)
        return response

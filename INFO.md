- Не совсем понятно как технические специалисты будут
отправлять запросы на создание роботов. Полагал, что
"В результате web-запроса на..." предполагает создание
web-интерфейса с формой, но тогда не совсем понятно 
как это согласовать с передачей данных в формате JSON. Рекрутер подсказала,
что интерфейса быть не должно. Поэтому посчитал, что
"web-запрос == http-запрос", который будет отправляться через
postman.


- По валидации "...на соответствие существующим в системе моделям"
не понял где в системе должны существовать предопределенные модели.
Поэтому создал в приложении robots отдельную модель RobotModel,
где их можно было бы хранить.

Запросы делаются на эндпоинт: 
```
http://127.0.0.1:8000/api/robot/
```

Пример данных для POST-запроса: 
```
{
    "model": "R2",
    "version": "D6",
    "created": "2022-12-31 23:59:59"
}
```
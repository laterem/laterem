# Дока как использовать domarrow.js - Соединение стрелкой 2 элементов

Скрипт взят [отсюда](https://www.cssscript.com/connect-elements-directional-arrow/) ([github](https://github.com/schaumb/domarrow.js))

## Подготовка

Нужно подключить скрипт написав `<script type="text/javascript" src="{% static 'js//domarrow.js/domarrow.js' %}"></script>` где-то перед использованием функционала

## Основной элемент

Все взаимодействие со скриптом происходит через парный тэг `<connection></connection>`
С обязательными (или нет) аргументами `from="" to="" color="" head tail onlyVisible`

### Аргементы

- `from=""` - Принимает идентификатор элемента (id/class), отвечает за определение элемента, из которого выходит стрелка
- `to=""` - Принимает идентификатор элемента (id/class), отвечает за определение элемента, к которому ведет стрелка
- `color=""` - Принимает значение цвета, в который будет окрашена стрелка
- `head` - При наличии у стрелки рисуется голова при конечном элементе
- `tail` - При наличии у стрелки рисуется голова при начальном элементе
- `onlyVizible` - При наличии стрелка рисуется только вне элементов (не проходя по ним)

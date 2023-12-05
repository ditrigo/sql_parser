# Main Parser
- pyparser.py

# done

- [x] условие(сальдо>100, 0, 10)
- [x] условие(сальдо>100, 0, условие(вклад>300, 11, 12))
- [x] условие(сальдо+условие(вклад>300, 5, условие(выручка>123, 333, 444))>100, 2, 10)

## Functions:

### Поиск подстроки в строке: «ПОИСК(“подстрока”;поле-строка)», «НЕПОИСК(“подстрока”;поле-строка)»
- [x] условие(ПОИСК(“долг”;imported_attributes.dolg);10;0)
- [x] условие(НЕПОИСК(“долг”;imported_attributes.dolg);10;0)

### Разница дат: «РАЗНДАТ(date;date;”mode”)»date – поле таблицы или СЕГОДНЯ(). “mode” - “y” или “d” – разница в полных годах или днях соответственно.
- [x] условие(РАЗНДАТ(imported_attributes.on_uch_date;СЕГОДНЯ();”y”)>15;3;0)

### Если ошибка: «ЕСЛИОШИБКА(выражение;если_ошибка)» - проверка "выражение" на деление на 0. Если есть деление на 0, выполняется "если_ошбка"
- [x] условие(ЕСЛИОШИБКА(a/(a+b+c) + a/b;20)>10;1;0)

### Проверка на пустое значение: «ЕПУСТО(поле)» - возвращает "True", если элемент пустой, иначе "False"
- [x] условие(ЕПУСТО(empty_item);1;0)

# todo



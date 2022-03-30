# MyBrainFuck
Это маленький полуобучающий проек как пользоваться PyPy на примере написания интерпритатора для языкa [brainfuck](https://ru.wikipedia.org/wiki/Brainfuck). Здесь мы напишем и проведем последовательное улучшение интерпритатора на Питоне. С более подробной информацией можно ознакомится [в статье на Хкбре](https://habr.com/ru/post/124418/) а исходный код [в репазитории на Github](https://github.com/disjukr/pypy-tutorial-ko). Тут мы просто обобщаем и автоматизируем при помощи скриптов выполнение всех процессов и тестов. В качестве результата мы получим копилятор, который будет переводить код brainfuck в машинный код.
## Подготовка
Для начала нам понадобиться `python3` и `pypy3.9`. Чтобы проверить, если ли у вас эти программы пропишите следующий команды.
```
python3 --version
```
```
pypy --version
```
Ответ не должен содержать сообщения об ошибке. В обратном случае, [гугл](https://www.google.com/search?q=how+to+install+pypy) вам в помощь.
## Скрипты
Основные скрипты будут написаны в Makefile 
## Начало: интерпритатор на чистом питоне
Для начала написшем интерпритатор самостоятельно и запустим его с помощью питона. 
Если вам интересен код можете заглянуть в папку `examples`. Программы на brainfuck лежит в папке `test_brainfuck`, здесь мы запустим `first_brainfuck.b`.  Сейчас мы будем использовать файл `python_only.py`. Следующая команда:
```
make python_only 
```
## Первое улучшение: переходим на PyPy

## Второе улучшение: добавляем JIT

## Третье улучшение: оптимизация

## Результат

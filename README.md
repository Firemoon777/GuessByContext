# Guess By Context

Inspired by [contexto.me](https://contexto.me/) and created for ru_RU language.

Used [Nunito by Vernon Adams](https://fonts.google.com/specimen/Nunito)

# "Русо Контексто"

Угадайте загаданное слово. У вас бесконечное количество попыток.

Слова отсортированы искуственным интеллектом по смыслу в порядке убывания.

После отправки слова отобразится его позиция в списке. Загаданное слово имеет номер 0.

Перед тем как попасть сюда, искуственный интеллект работал над миллионами текстов. Он использует полученный опыт и понимание контекста для определения смысловой близости слов.

## Как развернуть игру?

Для создания пользовательской части необходим NPM.

```bash
cd frontend
npm run build
```

В каталоге `dist` появится prod-сборка приложения. Подкладываем её на веб-сервер. 
В том же каталоге создаем подкаталог `game`. В этом подкаталоге должны находиться файлы игры.

Игра пригодна для работы в контейнере объектного хранилища.

## Как загадать слово?

Для того чтобы загадать слово нужно запрустить модуль `processor`. Для этого нужен интерпретатор Python версии 3.9 или выше.

```bash
# Устанавливаем зависимости
python3 -m pip install -r requirements.txt

# Запускаем
python3 -m processor -m model -o out/ -n "2022-12-12" "снег"
```

При первом запуске будет загружены две модели текстовых эмбеддингов и на их основе будет создан словарь существительных.
Все промежуточные файлы, необходимые для эмбеддингов будут сохранены в каталог, указанный через ключ `-m`. При повторных запусках скачиваний не производится.

Загруженная модель обработает слово `снег` и составит два словаря игры:

- в формате `txt`, где каждая строчка содержит только одно слово в порядке "загаданное слово на первой строчке, а дальше по убыванию"
- в формате `json`, где один большой ассоциативный массив вида `слово-позиция`.

Имя файла передается в формате `YYYY-MM-DD`. Модуль `processor` не производит проверку имени файла, однако, фронтенд ищет именно в таком формате. Если день или месяц состоят из одной цифры, то необходимо дополнить нулями. Например:

- 2022-12-12
- 2023-01-01

Примерная структура файлов на веб-сервере:

```bash
- /
  - index.html
  - assets/
    - index.XXXXXX.css
    - index.XXXXXX.js
  - game/
    - 2022-12-09.json
    - 2022-12-10.json
    - 2022-12-11.json
    - 2022-12-12.json
    - 2022-12-13.json
```

## Известные ограничения

1. Игра не ставит задачу максимально спрятать загаданное слово. Честность игрока всегда на игроке.
2. Игра не производит проверку доступности игры. При запуске ищется игра с именем, равным текущей дате. Если файла нет, поле ввода слова будет закрыто.
3. Список игр начинается с `2022-11-13`. Это значение жёстко задано в коде.
4. Словарь не идеален и иногда встречаются странные слова :(
5. Лемматизация слов не производится.

## Использованные материалы

- [Nunito by Vernon Adams](https://fonts.google.com/specimen/Nunito)
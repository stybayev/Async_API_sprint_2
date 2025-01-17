## Инструкция по запуску приложения:

1) Клонируем репозиторий:
   ```
   git clone git@github.com:stybayev/Async_API_sprint_2.git
   ```
2) Заходим в корневую директрию проекта `/Async_API_sprint_2`:
   ```
   cd path/to/Async_API_sprint_2
   ```
3) Создаем файл `.env` и копируем в него содержимое файла `.env.example`:
   ```
   cp .env.example .env
   ```
4) Запускаем сервисы:
   ```
   docker-compose -f docker-compose.dev.yml  up --build 
   ```
5) Все должно работать!


## Локальный запуск тестов

### Настройка виртуального окружения

1. **Создание виртуального окружения:**

   Для изоляции зависимостей проекта рекомендуется использовать виртуальное окружение. Создайте его с помощью следующей команды:
   ```bash
   python3 -m venv venv

2. **Активация виртуального окружения:**

   Для активации виртуального окружения воспользуйтесь командой:
   ```bash
   source venv/bin/activate

3. **Установка необходимых пакетов:**

   Установите все зависимости, перечисленные в файле requirements.txt, используя pip:
   ```bash
   pip install -r tests/functional/requirements.txt
   
4. **Запуск тестов с помощью pytest:**

   После настройки окружения и установки зависимостей, вы можете запустить тесты, используя pytest. Убедитесь, что все сервисы, необходимые для тестирования, запущены:   
   ```bash
   pytest
   
5. **Деактивация виртуального окружения:**
   
   После завершения тестирования рекомендуется деактивировать виртуальное окружение:
   ```bash
   deactivate

## Инструкция по запуску тестов в докере

### Подготовка к запуску тестов

1. **Переход в директорию тестов:**

   Навигация к папке с тестами.
   ```bash
   cd tests/functional
   
2. **Создание файла с переменными окружения для тестов:**

   Копирование предоставленного примера файла конфигурации в активный файл конфигурации.
   ```bash
   cp .env.test.example .env.test

3. **Запуск тестовых сервисов:**

   Используйте docker-compose для запуска тестов.
   ```bash
   docker-compose -f docker-compose.yml up --build
   
4. **Остановка и очистка тестовой среды:**

   После завершения тестирования рекомендуется остановить контейнеры и очистить созданные ресурсы.

   ```bash
   docker-compose down -v

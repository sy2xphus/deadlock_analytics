# Deadlock Analytics Project

## Описание
Пет-проект по аналитике игры **Deadlock** (Valve). Цель проекта — создать пайплайн для сбора данных, анализа механик/статистики и визуализации результатов в интерактивном дашборде.

## Структура проекта
```text
deadlock_analytics/
├── data/
│   ├── raw/           # Исходные данные (JSON, CSV)
│   └── processed/     # Очищенные данные для анализа
├── notebooks/         # Jupyter Notebooks для EDA и проверки гипотез
├── src/
│   └── etl/           # Скрипты сбора и обработки данных
├── app/               # Код веб-приложения (Streamlit)
├── .env.example       # Шаблон переменных окружения
├── .gitignore         # Исключения git
├── README.md          # Документация
└── requirements.txt   # Зависимости
```

## Установка и запуск

1. **Клонирование репозитория**
   ```bash
   git clone <repo_url>
   cd deadlock_analytics
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройка окружения**
   Создайте файл `.env` на основе `.env.example` и добавьте ваши ключи API.
   ```bash
   cp .env.example .env
   ```

## План разработки
1. **Сбор данных**: Написание ETL-скриптов для выгрузки данных из API.
2. **Анализ**: Исследовательский анализ данных (EDA) в Jupyter Notebooks.
3. **Визуализация**: Создание интерактивного дашборда на Streamlit.

## Автор
Data Analyst (Pet Project)

#!/usr/bin/env bash

# Для Render: база данных уже в переменной окружения DATABASE_URL
# Не нужно загружать из .env файла

echo "🔄 Инициализация базы данных..."

# Используем DATABASE_URL из окружения Render
if [ -z "$DATABASE_URL" ]; then
    echo "❌ Ошибка: DATABASE_URL не установлен"
    exit 1
fi

# Выполняем SQL скрипт
psql -a -d "$DATABASE_URL" -f init.sql

echo "✅ База данных инициализирована"
import sqlite3
import os

print("🔧 СОЗДАНИЕ SQL ДАМПА")
print("=" * 50)

# Ищем базу данных
db_path = 'instance/users.db'
if not os.path.exists(db_path):
    for root, dirs, files in os.walk('.'):
        if 'users.db' in files:
            db_path = os.path.join(root, 'users.db')
            print(f"✅ База найдена: {db_path}")
            break

try:
    conn = sqlite3.connect(db_path)

    with open('database_dump.sql', 'w', encoding='utf-8') as f:
        f.write("-- SQL Dump для защиты\n")
        f.write(f"-- Создано: {__import__('datetime').datetime.now()}\n\n")

        # Получаем список таблиц
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            f.write(f"\n-- Таблица: {table_name}\n")

            # Получаем структуру таблицы
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_sql = cursor.fetchone()[0]
            f.write(f"{create_sql};\n\n")

            # Получаем данные
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Получаем имена колонок
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]

            for row in rows:
                values = []
                for val in row:
                    if val is None:
                        values.append("NULL")
                    elif isinstance(val, (int, float)):
                        values.append(str(val))
                    else:
                        values.append(f"'{val}'")

                f.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n")

            f.write("\n")

    print("\n✅ SQL дамп создан: database_dump.sql")
    print(f"Размер: {os.path.getsize('database_dump.sql')} байт")

    # Показываем первые 10 строк
    print("\n📄 Первые 10 строк дампа:")
    print("-" * 50)
    with open('database_dump.sql', 'r') as f:
        for i, line in enumerate(f):
            if i < 10:
                print(line.strip())

    conn.close()

except Exception as e:
    print(f"❌ Ошибка: {e}")
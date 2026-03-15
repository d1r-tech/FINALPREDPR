import numpy as np
import os

print("1. ЗАГРУЗКА DATA.NPZ")
data = np.load('data/Data.npz')

# Смотрим, что внутри
print("Ключи:", data.files)

# Забираем нужные массивы
train_x = data['train_x']        # (1200, 80000, 1)
train_y_str = data['train_y']     # (1200,) строки
valid_x = data['valid_x']         # (400, 80000, 1)
valid_y_str = data['valid_y']     # (400,) строки

print(f"\nTrain X: {train_x.shape}")
print(f"Train Y: {len(train_y_str)} записей")
print(f"Valid X: {valid_x.shape}")
print(f"Valid Y: {len(valid_y_str)} записей")

# 2. ВОССТАНАВЛИВАЕМ МЕТКИ (строки -> числа)
print("\n2. ВОССТАНОВЛЕНИЕ МЕТОК")
unique_strings = np.unique(train_y_str)
label_map = {s: i for i, s in enumerate(unique_strings)}
train_y = np.array([label_map[s] for s in train_y_str])

# Для валидации используем ту же карту
valid_y = np.array([label_map.get(s, 0) for s in valid_y_str])

num_classes = len(unique_strings)
print(f"Найдено классов: {num_classes}")
print(f"Пример: '{unique_strings[0]}' -> {label_map[unique_strings[0]]}")

# 3. СОХРАНЯЕМ ОБРАБОТАННЫЕ ДАННЫЕ
os.makedirs('processed', exist_ok=True)
np.save('processed/train_x.npy', train_x)
np.save('processed/train_y.npy', train_y)
np.save('processed/valid_x.npy', valid_x)
np.save('processed/valid_y.npy', valid_y)
np.save('processed/label_map.npy', label_map)

print("\n✅ Данные сохранены в папку processed/")
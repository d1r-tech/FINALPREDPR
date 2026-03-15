import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import os
import time

print("1. ЗАГРУЗКА ОБРАБОТАННЫХ ДАННЫХ")
train_x = np.load('processed/train_x.npy')
train_y = np.load('processed/train_y.npy')
valid_x = np.load('processed/valid_x.npy')
valid_y = np.load('processed/valid_y.npy')
label_map = np.load('processed/label_map.npy', allow_pickle=True).item()

num_classes = len(label_map)
print(f"Классов: {num_classes}")
print(f"Train X: {train_x.shape}")
print(f"Valid X: {valid_x.shape}")

train_y_cat = tf.keras.utils.to_categorical(train_y, num_classes)
valid_y_cat = tf.keras.utils.to_categorical(valid_y, num_classes)

print("\n2. СОЗДАНИЕ МОДЕЛИ")
model = models.Sequential([
    layers.MaxPooling1D(pool_size=4, input_shape=(80000, 1)),

    layers.Conv1D(16, 3, activation='relu', padding='same'),
    layers.MaxPooling1D(2),

    layers.Conv1D(32, 3, activation='relu', padding='same'),
    layers.MaxPooling1D(2),

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

print("\n3. ОБУЧЕНИЕ (5 эпох)...")
start = time.time()

history = model.fit(
    train_x, train_y_cat,
    epochs=5,
    batch_size=16,
    validation_data=(valid_x, valid_y_cat),
    verbose=1
)

print(f"Обучение завершено за {(time.time() - start) / 60:.1f} минут")

os.makedirs('models', exist_ok=True)
model.save('models/classifier.keras')
np.save('models/label_map.npy', label_map)

val_loss, val_acc = model.evaluate(valid_x, valid_y_cat, verbose=0)
print(f"\n✅ Точность на валидации: {val_acc:.4f}")

import pandas as pd

pd.DataFrame(history.history).to_csv('models/training_log.csv', index=False)
print("✅ Модель сохранена в models/classifier.keras")
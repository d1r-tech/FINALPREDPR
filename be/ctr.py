import numpy as np
import tensorflow as tf

print("Загрузка модели...")
model = tf.keras.models.load_model('../models/classifier.keras')

print("Загрузка данных...")
train_x = np.load('../processed/train_x.npy')
train_y = np.load('../processed/train_y.npy')
valid_x = np.load('../processed/valid_x.npy')
valid_y = np.load('../processed/valid_y.npy')

train_y_cat = tf.keras.utils.to_categorical(train_y, model.output_shape[-1])
valid_y_cat = tf.keras.utils.to_categorical(valid_y, model.output_shape[-1])

print("Продолжение обучения (ещё 5 эпох)...")
history = model.fit(
    train_x, train_y_cat,
    epochs=20,
    batch_size=16,
    validation_data=(valid_x, valid_y_cat),
    verbose=1
)

model.save('models/classifier.keras')
print("Модель дообучена и сохранена")
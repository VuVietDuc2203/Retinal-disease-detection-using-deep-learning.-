# -*- coding: utf-8 -*-
"""VGG16.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-J1ZKglLSNfNMOwnWQFT7Nnc--wzmO-t
"""

from keras.layers.reshaping.flatten import Flatten
import cv2
import numpy
import pandas
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from keras.layers import BatchNormalization
focal_loss = CategoricalCrossentropy(from_logits=False, label_smoothing=0.1)

from keras.applications.vgg16 import VGG16
vgg_model = VGG16(weights='imagenet', include_top=False, input_shape=(300, 300, 3))

model = Sequential()
model.add(vgg_model)

model.add(Flatten())
model.add(Dense(2048, activation = 'relu'))
model.add(Dense(2048, activation = 'relu'))
model.add(Dense(1024, activation = 'relu'))
model.add(Dense(512, activation = 'relu'))
model.add(Dense(3, activation = 'softmax'))
model.summary()
model.compile(optimizer = Adam(learning_rate = 0.00001),
              loss = 'categorical_crossentropy',
              metrics=['accuracy']

              )

from keras.preprocessing.image import ImageDataGenerator

train_folder = '/home/ibmelab/Documents/ibme/RFMiD/train'
valid_folder = '/home/ibmelab/Documents/ibme/RFMiD/test'


train_datagen = ImageDataGenerator(rescale = 1./255., rotation_range = 10,
                                   width_shift_range=0.1, height_shift_range=0.1,
                                   shear_range = 0.1, zoom_range = 0.1, horizontal_flip = True,


                                 )

valid_datagen = ImageDataGenerator(rescale = 1./255.,)


train_generator = train_datagen.flow_from_directory(train_folder, batch_size = 120,
                                                    class_mode = 'categorical', target_size = (300, 300),
)

valid_generator = valid_datagen.flow_from_directory(valid_folder, batch_size = 120,
                                                    class_mode = 'categorical', target_size = (300, 300))

history = model.fit(
    train_generator,
    validation_data = valid_generator,
    steps_per_epoch = 10,
    epochs = 50,
    validation_steps = 10,

    verbose = 1
)

# model.save('/home/ibmelab/Documents/ibme/RFMiD/model/VGG16_99%.h5')

import os
import cv2
import numpy as np
def test(model, path1, path2, path3):
    def process_images(path):
        os.chdir(path)
        files = os.listdir(path)
        class_counts = [0, 0, 0]

        for filename in files:
            img = cv2.imread(filename)

            if img is None:
                continue

            img = pre_process(img)
            predictions = model.predict(np.expand_dims(img, axis=0))
            y_pred = np.argmax(predictions, axis=1)
            class_counts[y_pred[0]] += 1

        return class_counts

    class_counts_1 = process_images(path1)
    class_counts_2 = process_images(path2)
    class_counts_3 = process_images(path3)

    # Tiếp tục xử lý kết quả như bình thường
    class1_class1, class2_class1, class3_class1 = class_counts_1
    class1_class2, class2_class2, class3_class2 = class_counts_2
    class1_class3, class2_class3, class3_class3 = class_counts_3

    class_1_predicts = class1_class1 + class1_class2 + class1_class3
    class_2_predicts = class2_class1 + class2_class2 + class2_class3
    class_3_predicts = class3_class1 + class3_class2 + class3_class3

    recall = [
        class1_class1 / len(os.listdir(path1)),
        class2_class2 / len(os.listdir(path2)),
        class3_class3 / len(os.listdir(path3))
    ]

    precisions = [
        class1_class1 / class_1_predicts,
        class2_class2 / class_2_predicts,
        class3_class3 / class_3_predicts
    ]

    return {'Precision': precisions, 'Recall': recall}


def evaluate(model, path1, path2, path3):
    def process_images(path):
        os.chdir(path)
        files = os.listdir(path)
        label = 0
        if path == path2:
            label = 1
        elif path == path3:
            label = 2
        else:
            label = 0
        predict = []
        labels = []
        for filename in files:
            image = cv2.imread(filename)
            image = image/255.
            resized_image = cv2.resize(image, (300, 300))
            predictions = model.predict(np.expand_dims(resized_image, axis=0))
            y_pred = np.argmax(predictions, axis=1)[0]
            predict.append(y_pred)
            labels.append(label)

        return predict, labels



    predict1, label1 = process_images(path1)
    predict2, label2 = process_images(path2)
    predict3, label3 = process_images(path3)

    labels = label1 + label2 + label3
    predicts = predict1 + predict2 + predict3

    return predicts, labels

path1 = '/home/ibmelab/Documents/ibme/RFMiD/test/AMD'
path2 = '/home/ibmelab/Documents/ibme/RFMiD/test/DR'
path3 = '/home/ibmelab/Documents/ibme/RFMiD/test/Non'
predicts, labels = evaluate(model, path1, path2, path3)

from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(labels, predicts))
import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(confusion_mat, labels):
    plt.figure(figsize=(14, 10))
    sns.set(font_scale=2.0)
    sns.heatmap(confusion_mat, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.title("Confusion Matrix")
    plt.show()

# Định nghĩa ma trận lẫn nhau
confusion_mat = confusion_matrix(labels, predicts)

# Định nghĩa danh sách nhãn
class_name = ["AMD", "DR", "Non"]

# Visualize confusion matrix
plot_confusion_matrix(confusion_mat, class_name)

print(model.evaluate_generator(valid_generator))

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

test_folder = '/home/ibmelab/Documents/ibme/RFMiD/test'

test_datagen = ImageDataGenerator(rescale = 1./255.,)




test_generator = valid_datagen.flow_from_directory(test_folder, batch_size = 120,
                                                    class_mode = 'categorical', target_size = (300, 300))

y_pred = model.predict(test_generator)

y_pred = model.predict(test_generator)
y_true = test_generator.classes
y_pred = np.argmax(y_pred, axis=1)
target_names = test_generator.class_indices.keys()
print(classification_report(y_true, y_pred, target_names=target_names))

results = model.evaluate_generator(test_generator)
print("test loss, test accuracy:", results)

# model.save('/home/ibmelab/Documents/ibme/RFMiD/model.h5')

"""# Inception V3

"""

inception_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(300, 300, 3))

model_1 = Sequential()
model_1.add(inception_model)

model_1.add(Flatten())
model_1.add(Dense(4048, activation = 'relu'))
model_1.add(Dense(1024, activation = 'relu'))
model_1.add(Dense(3, activation = 'softmax'))
model_1.summary()
model_1.compile(optimizer = Adam(learning_rate = 0.00001),
              loss=focal_loss,
              metrics=['accuracy']
              )

history = model_1.fit_generator(
    train_generator,
    validation_data = valid_generator,
    steps_per_epoch = 10,
    epochs = 60,
    validation_steps = 10,
    verbose = 1
)

print(model_1.evaluate(test_generator))

import matplotlib.pyplot as plt

# Truy xuất thông tin về quá trình huấn luyện
train_loss = history.history['loss']
val_loss = history.history['val_loss']
train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

# Vẽ biểu đồ hàm mất mát trên tập train và validation
plt.plot(train_loss, label='Train Loss')
plt.plot(val_loss, label='Val Loss')
plt.legend()
plt.show()

# Vẽ biểu đồ độ chính xác trên tập train và validation
plt.plot(train_acc, label='Train Accuracy')
plt.plot(val_acc, label='Val Accuracy')
plt.legend()
plt.show()

y_pred = model_1.predict(test_generator)
y_true = test_generator.classes
y_pred = np.argmax(y_pred, axis=1)
target_names = test_generator.class_indices.keys()
print(classification_report(y_true, y_pred, target_names=target_names))
plt.show()

"""# Unet

"""



"""# MobileNet

"""

from keras.applications.resnet import ResNet101
from keras.layers import MaxPooling2D
from keras.layers import AveragePooling2D
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model

base_model = MobileNet(weights='imagenet', include_top=False, input_shape = (300, 300, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(3, activation='softmax')(x)

mobileNet = Model(inputs=base_model.input, outputs=predictions)
mobileNet.summary()
mobileNet.compile(optimizer = Adam(learning_rate = 0.00001),
              loss=focal_loss,
              metrics=['accuracy']
              )

history = mobileNet.fit_generator(
    train_generator,
    validation_data = valid_generator,
    steps_per_epoch = 5,
    epochs = 30,
    validation_steps = 5,
    verbose = 1
)


# -*- coding: utf-8 -*-
"""val.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XYeg-3EaVdN3AZv2t5wGpx7k4bUD_nkG
"""

import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

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

model_path = '/home/ibmelab/Documents/ibme/RFMiDgoc/model/VGG164.h5'
model = load_model(model_path)

path1 = '/home/ibmelab/Documents/ibme/RFMiDgoc/test/AMD'
path2 = '/home/ibmelab/Documents/ibme/RFMiDgoc/test/DR'
path3 = '/home/ibmelab/Documents/ibme/RFMiDgoc/test/Non'
predicts, labels = evaluate(model, path1, path2, path3)

print(len(labels), len(predicts))

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


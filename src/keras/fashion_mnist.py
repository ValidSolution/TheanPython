# codes origin from website：https://www.tensorflow.org/tutorials/keras/basic_classification?hl=zh-CN
from __future__ import absolute_import, division, print_function, unicode_literals

# 导入TensorFlow和tf.keras
import tensorflow as tf
from tensorflow import keras

# 导入辅助库
import numpy as np
import matplotlib.pyplot as plt


# 两个函数用来以图形的方式查看完整的10个类预测
def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]), color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


print(tf.__version__)
# 导入并加载数据
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
"""
训练集中有60,000个图像，每个图像表示为28 x 28像素
train_images.shape
(60000, 28, 28)

共60000个标签
len(train_labels)
60000

每个标签都是0到9之间的整数:
train_labels
array([9, 0, 0, ..., 3, 0, 5], dtype=uint8)

测试集中有10,000个图像。 同样，每个图像表示为28×28像素:
test_images.shape
(10000, 28, 28)

测试集包含10,000个图像标签:
len(test_labels)
10000
"""
# 共十种标签
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
# 数据预处理，像素值为0~255
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()
# 将像素值缩放到0~1之间
train_images = train_images / 255.0
test_images = test_images / 255.0
# 显示训练集中的前25个图像，并在每个图像下方显示类名。验证数据格式是否正确，我们是否已准备好构建和训练网络。
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()
# 设置网络层。网络层从提供给他们的数据中提取表示，并期望这些表示对当前的问题更加有意义
model = keras.Sequential([
    # 将图片从二维数组转成28*28的一维数组
    keras.layers.Flatten(input_shape=(28, 28)),
    # 第一层神经元有128个节点
    keras.layers.Dense(128, activation=tf.nn.relu),
    # 输出层包含10个几点，对应10个标签的概率，总和为1
    keras.layers.Dense(10, activation=tf.nn.softmax)
])
# 编译模型，分别是优化器，损失函数，指标
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# 训练模型，即使模型"适合"训练数据
model.fit(train_images, train_labels, epochs=5)
# 评估准确性
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test accuracy:', test_acc)
# 预测测试集
predictions = model.predict(test_images)

# 绘制前X个测试图像，预测标签和真实标签
# 以蓝色显示正确的预测，红色显示不正确的预测
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, test_labels)
plt.show()

img = test_images[0]

print(img.shape)

# 将图像添加到批次中，即使它是唯一的成员。
img = (np.expand_dims(img, 0))

print(img.shape)
predictions_single = model.predict(img)

print(predictions_single)
plot_value_array(0, predictions_single, test_labels)
plt.xticks(range(10), class_names, rotation=45)
plt.show()
prediction_result = np.argmax(predictions_single[0])
print(prediction_result)

from src.com.thean.python.tf import input_data
import tensorflow as tf

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
# 占位符，数组第一个None表示对图片的索引，即第几张图片，None表示可以是任意长度，每张图片被展开为784(28*28)维
x = tf.placeholder("float", [None, 784])
# 可修改的张量，784维的图片乘以w得到一个10维的向量
w = tf.Variable(tf.zeros([784, 10]))
# bias偏置量
b = tf.Variable(tf.zeros([10]))
# softMax是归一化？
y = tf.nn.softmax(tf.matmul(x, w) + b)
# y_是y的导数？
y_ = tf.placeholder("float", [None, 10])
# 计算交叉熵
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
# GradientDescentOptimizer是梯度下降算法，
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
for i in range(1000):
    # 随机抓取100个数据点，（随机训练，或者本例中更准确的叫随机梯度下降训练）
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# 检验模型的准确率
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
exit(0)

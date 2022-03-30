import tensorflow as tf
from numpy.random import RandomState
 
'''
Код страницы учебника P62: полный пример программы нейронной сети
'''
 # 1. Определите параметры, входные и выходные узлы нейронной сети.
batch_size = 8
w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))
x = tf.placeholder(tf.float32, shape=(None, 2), name="x-input")
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')
 
 # 2. Определите процесс прямого распространения, функцию потерь и алгоритм обратного распространения.
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)
cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
 
 # 3. Создание набора данных моделирования.
rdm = RandomState(1)
X = rdm.rand(128,2)
Y = [[int(x1+x2 < 1)] for (x1, x2) in X]
 
 # 4. Создайте сеанс для запуска программы TensorFlow.
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
 
         # Вывести текущие (необученные) значения параметров.
    print("w1:\n", sess.run(w1))
    print("w2:\n", sess.run(w2))
    print("\n")
 
 
         # Обучите модель.
    STEPS = 5000
    for i in range(STEPS):
        start = (i * batch_size) % 128
        end = (i * batch_size) % 128 + batch_size
        sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})
        if i % 1000 == 0:
            total_cross_entropy = sess.run(cross_entropy, feed_dict={x: X, y_: Y})
            print("After %d training step(s), cross entropy on all data is %g" % (i, total_cross_entropy))
 
         # Вывести значения параметров после обучения.
    print("\n")
    print("w1:\n", sess.run(w1))
    print("w2:\n", sess.run(w2))
 

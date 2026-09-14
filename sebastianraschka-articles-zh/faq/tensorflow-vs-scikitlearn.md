---
title: "TensorFlow 和 scikit-learn 的主要区别是什么？"
title_en: "What is the main difference between TensorFlow and scikit-learn?"
source: https://sebastianraschka.com/faq/docs/tensorflow-vs-scikitlearn.html
crawled: 2026-09-06
translated: 2026-09-14
---

# TensorFlow 和 scikit-learn 的主要区别是什么？

TensorFlow 更偏向底层库；基本上，我们可以把 TensorFlow 想象成乐高积木（类似于 NumPy 和 SciPy），用它们可以实现机器学习算法；而 scikit-learn 提供的是开箱即用的算法，例如分类算法，包括 SVM、随机森林、Logistic 回归等等，不胜枚举。如果要实现深度学习算法，TensorFlow 尤其大放异彩，因为它让我们能够利用 GPU 来实现更高效的训练。
为了更好地理解这两个库的区别，下面我们用 scikit-learn 在鸢尾花（Iris）数据集上拟合一个 softmax 回归模型：

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Loading Data
iris = load_iris()
X = iris.data[:, [0, 3]] # sepal length and petal width
y = iris.target

# standardize
X[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
X[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()

lr = LogisticRegression(penalty='l2',
                        dual=False,
                        tol=0.000001,
                        C=10.0,
                        fit_intercept=True,
                        intercept_scaling=1,
                        class_weight=None,
                        random_state=1,
                        solver='newton-cg',
                        max_iter=100,
                        multi_class='multinomial',
                        verbose=0,
                        warm_start=False,
                        n_jobs=1)
lr.fit(X, y)
```

此外，我写了一个小辅助函数来绘制二维决策面：

```python
from mlxtend.plotting import plot_decision_regions

plot_decision_regions(X, y, clf=lr)
plt.title('Softmax Regression in scikit-learn')
plt.show()
```

![](https://sebastianraschka.com/images/faq/tensorflow-vs-scikitlearn/scikit-softmax.png)

很简单，对吧？:)。而如果我们要通过 TensorFlow 拟合一个 Softmax 回归模型，就必须先「搭建」这个算法。不过这实际听起来比做起来难。
TensorFlow 自带许多「便捷」函数和工具。例如，如果我们想使用梯度下降优化方法，实现的核心部分可能像这样：

```python
# Construct the Graph
  g = tf.Graph()
  with g.as_default():

      if init_weights:
          self._n_classes = np.max(y) + 1
          self._n_features = X.shape[1]
          tf_weights_, tf_biases_ = self._initialize_weights(
              n_features=self._n_features,
              n_classes=self._n_classes)
          self.cost_ = []
      else:
          tf_weights_ = tf.Variable(self.weights_)
          tf_biases_ = tf.Variable(self.biases_)

      # Prepare the training data
      y_enc = self._one_hot(y, self._n_classes)
      n_idx = list(range(y.shape[0]))
      tf_X = tf.convert_to_tensor(value=X, dtype=self.dtype)
      tf_y = tf.convert_to_tensor(value=y_enc, dtype=self.dtype)
      tf_idx = tf.placeholder(tf.int32,
                              shape=[int(y.shape[0] / n_batches)])
      X_batch = tf.gather(params=tf_X, indices=tf_idx)
      y_batch = tf.gather(params=tf_y, indices=tf_idx)

      # Setup the graph for minimizing cross entropy cost
      logits = tf.matmul(X_batch, tf_weights_) + tf_biases_
      cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits,
                                                              y_batch)
      cost = tf.reduce_mean(cross_entropy)
      optimizer = tf.train.GradientDescentOptimizer(
          learning_rate=self.eta)
      train = optimizer.minimize(cost)

      # Initializing the variables
      init = tf.initialize_all_variables()
```

然后我们可以像这样执行训练：

```python
# Launch the graph
with tf.Session(graph=g) as sess:
    sess.run(init)
    self.init_time_ = time()
    for epoch in range(self.epochs):
        if self.minibatches > 1:
            n_idx = np.random.permutation(n_idx)
        minis = np.array_split(n_idx, self.minibatches)
        costs = []
        for idx in minis:
            _, c = sess.run([train, cost], feed_dict={tf_idx: idx})
            costs.append(c)
```

```python
为了演示，我以面向对象的风格通过 TensorFlow 实现了 Softmax 回归，写法与 scikit-learn 的实现有些相似。如果你感兴趣，完整代码示例在这里：[mlxtend/tf_classifier/TfSoftmax](https://github.com/rasbt/mlxtend/blob/master/mlxtend/tf_classifier/tf_softmax.py)。
```

```python
from mlxtend.tf_classifier import TfSoftmaxRegression

lr = TfSoftmaxRegression(eta=0.75,
                         epochs=1000,
                         print_progress=True,
                         minibatches=1,
                         random_seed=1)

lr.fit(X, y)
Epoch: 1000/1000 | Cost 0.12

plt.plot(range(len(lr.cost_)), lr.cost_)
plt.xlabel('Iterations')
plt.ylabel('Cost')
plt.show()
```

![](https://sebastianraschka.com/images/faq/tensorflow-vs-scikitlearn/tf_cost.png)

```python
from mlxtend.evaluate import plot_decision_regions

plot_decision_regions(X, y, clf=lr)
plt.title('Softmax Regression via Gradient Descent in TensorFlow')
plt.show()
```

![](https://sebastianraschka.com/images/faq/tensorflow-vs-scikitlearn/tf_softmax.png)

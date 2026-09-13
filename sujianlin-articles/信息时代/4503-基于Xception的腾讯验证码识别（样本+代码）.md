---
title: "基于Xception的腾讯验证码识别（样本+代码）"
date: "2017-07-24"
author: "苏剑林"
category: "信息时代"
tags: ["图像", "深度学习", "数据集"]
url: "https://kexue.fm/archives/4503"
blog: "科学空间 | Scientific Spaces"
---

去年的时候，有幸得到网友提供的一批腾讯验证码样本，因此也研究了一下，过程记录在[《端到端的腾讯验证码识别（46%正确率）》](https://kexue.fm/archives/4138/)中。

后来，这篇文章引起了不少读者的兴趣，有求样本的，有求模型的，有一起讨论的，让我比较意外。事实上，原来的模型做得比较粗糙，尤其是准确率难登大雅之台，参考价值不大。这几天重新折腾了一下，弄了个准确率高一点的模型，同时也把样本公开给大家。

模型的思路跟[《端到端的腾讯验证码识别（46%正确率）》](https://kexue.fm/archives/4138/)是一样的，只不过把CNN部分换成了现成的Xception结构，当然，读者也可以换VGG、Resnet50等玩玩，事实上对验证码识别来说，这些模型都能够胜任。我挑选Xception，是因为它层数不多，模型权重也较小，我比较喜欢而已。

## 代码
Github：[https://github.com/bojone/n2n-ocr-for-qqcaptcha/](https://github.com/bojone/n2n-ocr-for-qqcaptcha/blob/master/qqcaptcha-with-xception.py)

```
import glob
samples = glob.glob('sample/*.jpg')

import numpy as np
np.random.shuffle(samples) #打乱训练样本

nb_train = 90000 #共有10万样本，9万用于训练，1万用于测试
train_samples = samples[:nb_train]
test_samples = samples[nb_train:]

from keras.applications.xception import Xception,preprocess_input
from keras.layers import Input,Dense,Dropout
from keras.models import Model

img_size = (50, 120) #全体图片都resize成这个尺寸
input_image = Input(shape=(img_size[0],img_size[1],3))
base_model = Xception(input_tensor=input_image, weights='imagenet', include_top=False, pooling='avg')
predicts = [Dense(26, activation='softmax')(Dropout(0.5)(base_model.output)) for i in range(4)]

model = Model(inputs=input_image, outputs=predicts)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

from scipy import misc
def data_generator(data, batch_size): #样本生成器，节省内存
    while True:
        batch = np.random.choice(data, batch_size)
        x,y = [],[]
        for img in batch:
            x.append(misc.imresize(misc.imread(img), img_size))
            y.append([ord(i)-ord('a') for i in img[-8:-4]])
        x = preprocess_input(np.array(x).astype(float))
        y = np.array(y)
        yield x,[y[:,i] for i in range(4)]

#训练过程终会显示逐标签的准确率
model.fit_generator(data_generator(train_samples, 100), steps_per_epoch=1000, epochs=10, validation_data=data_generator(test_samples, 100), validation_steps=100)

#评价模型的全对率
from tqdm import tqdm
total = 0.
right = 0.
step = 0
for x,y in tqdm(data_generator(test_samples, 100)):
    _ = model.predict(x)
    _ = np.array([i.argmax(axis=1) for i in _]).T
    y = np.array(y).T
    total += len(x)
    right += ((_ == y).sum(axis=1) == 4).sum()
    if step < 100:
        step += 1
    else:
        break

print u'模型全对率：%s'%(right/total)
```

要注意的是：Xception的预训练权重是imagenet图片分类任务的，显然不适用于验证码识别，因此这里将所有层都放开训练了，没有像一般分类任务那样固定大部分权重。

## 结果
经过上述代码训练后，模型在测试集的识别率（四个全对才算对）可以达到85%以上。更精细的调参（可以考虑调整学习率、增减迭代次数、调整模型结构等等）可以达到90%以上。

另外，还可以参考杨培文大神的杰作，最后分类使用CTC来做：[《使用深度学习来破解 captcha 验证码》](https://zhuanlan.zhihu.com/p/26078299)。

## 资源
10万验证码样本公开如下：

> 链接: <https://pan.baidu.com/s/1mhO1sG4> 密码: j2rj

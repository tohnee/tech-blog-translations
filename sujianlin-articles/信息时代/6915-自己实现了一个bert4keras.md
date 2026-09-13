---
title: "自己实现了一个bert4keras"
date: "2019-08-27"
author: "苏剑林"
category: "信息时代"
tags: ["语言模型", "NLP", "keras", "attention"]
url: "https://kexue.fm/archives/6915"
blog: "科学空间 | Scientific Spaces"
---

分享个人实现的bert4keras：
> <https://github.com/bojone/bert4keras>

这是笔者重新实现的keras版的bert，致力于用尽可能清爽的代码来实现keras下调用bert。

## 说明
目前已经基本实现bert，并且能成功加载官方权重，经验证模型输出跟keras-bert一致，大家可以放心使用。

本项目的初衷是为了修改、定制上的方便，所以可能会频繁更新。

因此欢迎star，但不建议fork，因为你fork下来的版本可能很快就过期了。

## 使用
快速安装；

```
pip install git+https://www.github.com/bojone/bert4keras.git

```

参考代码：

```
#! -*- coding: utf-8 -*-
# 测试代码可用性

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
import numpy as np

config_path = '../../kg/bert/chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = '../../kg/bert/chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = '../../kg/bert/chinese_L-12_H-768_A-12/vocab.txt'

tokenizer = Tokenizer(dict_path) # 建立分词器
model = build_transformer_model(config_path, checkpoint_path) # 建立模型，加载权重

# 编码测试
token_ids, segment_ids = tokenizer.encode(u'语言模型')
print(model.predict([np.array([token_ids]), np.array([segment_ids])]))
```

之前在[《当Bert遇上Keras：这可能是Bert最简单的打开姿势》](https://kexue.fm/archives/6736)中基于keras-bert给出的例子，仍适用于本项目，只需要将base_model的加载方式换成本项目的。

目前只保证支持Python 2.7，实验环境是Tesorflow 1.8+以及Keras 2.2.4+。
（有朋友测试过，python 3也可以直接用，没报错，反正python 3的用户可以直接试试。但我自己没测试过，所以不保证。）

当然，乐于贡献的朋友如果发现了某些bug的话，也欢迎指出修正甚至Pull Requests～

## 背景
之前一直用CyberZHG大佬的[keras-bert](https://github.com/CyberZHG/keras-bert)，如果纯粹只是为了在keras下对bert进行调用和fine tune来说，keras-bert已经足够能让人满意了。

然而，如果想要在加载官方预训练权重的基础上，对bert的内部结构进行修改，那么keras-bert就比较难满足我们的需求了，因为keras-bert为了代码的复用性，几乎将每个小模块都封装为了一个单独的库，比如keras-bert依赖于keras-transformer，而keras-transformer依赖于keras-multi-head，keras-multi-head依赖于keras-self-attention，这样一重重依赖下去，改起来就相当头疼了。

所以，我决定重新写一个keras版的bert，争取在几个文件内把它完整地实现出来，减少这些依赖性，并且保留可以加载官方预训练权重的特性。

## 鸣谢
感谢CyberZHG大佬实现的keras-bert，本实现有不少地方参考了keras-bert的源码，在此衷心感谢大佬的无私奉献。

---
title: "Twitter 时间线词云"
title_en: "Twitter Timeline Word Cloud"
source: https://sebastianraschka.com/Articles/2014_twitter_wordcloud.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Twitter 时间线词云

> 原文：[Twitter Timeline Word Cloud](https://sebastianraschka.com/Articles/2014_twitter_wordcloud.html) · Sebastian Raschka's Articles

## 用 Python 把你的 Twitter 时间线变成词云

上周，我发布了一些与「Happy Rock Song」数据挖掘项目相关的可视化结果，有些人很好奇我是怎么创建那些词云的。我想，在这个教程里换一个不同的数据集也许会更有意思：你的个人 Twitter 时间线。

![Twitter wordcloud my twitter wordcloud 2 small](https://sebastianraschka.com/images/blog/2014/twitter-wordcloud/my_twitter_wordcloud_2_small.webp)

### 章节

### 环境要求

在开始之前，我想先列出让它跑起来所需的一些包！

下面是基本包的列表，可以通过以下命令安装

```python
pip install <package_name>
```

- [twitter](https://pypi.python.org/pypi/twitter)
- [pyprind](https://pypi.python.org/pypi/PyPrind/)
- [numpy](http://numpy.org)
- [matplotlib](http://matplotlib.org)
- [pandas](http://pandas.pydata.org)
- [scipy](http://www.scipy.org)

而 Andreas Mueller 编写的 Python（2.7）[`wordcloud`](https://github.com/amueller/word_cloud) 包可以通过以下命令安装

```python
pip install git+git://github.com/amueller/word_cloud.git
```

注意，`wordcloud` 需要 Python 的图像处理库
[PIL](https://pillow.readthedocs.io/en/stable/handbook/index.html)。视操作系统而定，PIL 的安装和配置可能相当费劲；不过，当我在不同的 MacOS 和 Linux 系统上尝试通过 [`conda`](https://docs.conda.io/projects/conda/en/stable/user-guide/install/) 安装它时，似乎总能顺利搞定：

```python
conda install pil
```

让我用我趁手的 [`watermark`](https://github.com/rasbt/watermark)
扩展来总结一下我在下载 Twitter 时间线并创建词云时用到的各个包及其版本号：

```python
%load_ext watermark
%watermark -d -v -m -p twitter,pyprind,wordcloud,pandas,scipy,matplotlib

28/11/2014

CPython 2.7.8
IPython 2.1.0

twitter 1.15.0
pyprind 2.8.0
wordcloud 1.0.0
pandas 0.14.1
scipy 0.14.0
matplotlib 1.3.1

compiler   : GCC 4.2.1 (Apple Inc. build 5577)
system     : Darwin
release    : 14.0.0
machine    : x86_64
processor  : i386
CPU cores  : 2
interpreter: 64bit
```

## A. 下载你的 Twitter 时间线推文

为了下载我们的 Twitter 时间线，我们将使用一个简单的命令行工具
[`twitter_timeline.py`](https://github.com/rasbt/datacollect/tree/master/twitter_timeline)。
它的用法非常简单，我在相应 GitHub 仓库中的
[README.md](https://github.com/rasbt/datacollect/tree/master/twitter_timeline)
文件里详细介绍了配置步骤。在你提供了必要的认证信息之后，就可以在终端里运行

```python
python ./twitter_timeline.py --out 'output.csv'
```

把你的时间线保存为 CSV 格式。

或者，你也可以从 `twitter_timeline.py` 中导入 `TimelineMiner` 类，直接在这个 IPython notebook 里运行代码，如下所示。

```python
import sys
sys.path.append('../../twitter_timeline/')
import twitter_timeline
import oauth_info as auth

tm = twitter_timeline.TimelineMiner(auth.ACCESS_TOKEN,
                                    auth.ACCESS_TOKEN_SECRET,
                                    auth.CONSUMER_KEY,
                                    auth.CONSUMER_SECRET,
                                    auth.USER_NAME
                                    )

print('Authentification successful: %s' %tm.authenticate())
tm.get_timeline(max=2000, keywords=[])

Authentification successful: True
Tweets downloaded: 1999
```

![Twitter wordcloud twitter timeline](https://sebastianraschka.com/images/blog/2014/twitter-wordcloud/twitter_timeline.webp)

如果你是在终端里使用的 `twitter_timeline.py`，那么可以通过以下代码从 CSV 文件中读取「tweets」

```python
import pandas as pd
df = pd.read_csv('path/to/CSV')
```

## B. 创建词云

现在我们已经收集好了 Twitter 时间线中的推文，多亏了 `wordcloud` 这个好用的模块，词云的创建非常简单直接。

```python
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# join tweets to a single string
words = ' '.join(tm.df['tweet'])

# remove URLs, RTs, and twitter handles
no_urls_no_tags = " ".join([word for word in words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                            ])

wordcloud = WordCloud(
                      font_path='/Users/sebastian/Library/Fonts/CabinSketch-Bold.ttf',
                      stopwords=STOPWORDS,
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(no_urls_no_tags)

plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('./my_twitter_wordcloud_1.png', dpi=300)
plt.show()
```

![Twitter wordcloud my twitter wordcloud 1](https://sebastianraschka.com/images/blog/2014/twitter-wordcloud/my_twitter_wordcloud_1.webp)

意料之中的惊喜：我在推文中最常用的词显然就是「Python！」。

为了让词云在视觉上更有吸引力，我们再使用 Twitter logo 的形状作为自定义形状：

```python
from scipy.misc import imread

twitter_mask = imread('./twitter_mask.png', flatten=True)

wordcloud = WordCloud(
                      font_path='/Users/sebastian/Library/Fonts/CabinSketch-Bold.ttf',
                      stopwords=STOPWORDS,
                      background_color='white',
                      width=1800,
                      height=1400,
                      mask=twitter_mask
            ).generate(no_urls_no_tags)

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('./my_twitter_wordcloud_2.png', dpi=300)
plt.show()
```

![Twitter wordcloud my twitter wordcloud 2](https://sebastianraschka.com/images/blog/2014/twitter-wordcloud/my_twitter_wordcloud_2.webp)

（你可以在[这里](https://raw.githubusercontent.com/rasbt/datacollect/master/dataviz/twitter_cloud/twitter_mask.png)找到 `twitter_mask.png`）

另外，你还可以向 `STOPWORD` 集合中添加额外的停用词，让它们在构建词云时被忽略：

```python
more_stopwords = {'oh', 'will', 'hey', 'yet', ...}
STOPWORDS = STOPWORDS.union(more_stopwords)
```

我最初是在一个完全不同的场景下写下这段简单的 Twitter 时间线挖掘代码的，而后来在做一个按情绪对歌词进行分类的数据挖掘项目时，幸运地发现了这个精巧的 wordcloud 模块。不过我必须说，我觉得这个组合格外有趣，而且我也很好奇能对自己的 Twitter 用语和话题获得一个「客观」的印象！希望你觉得这篇简短的教程有意思，也期待在 Twitter 上看到你们的词云！

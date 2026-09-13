---
title: "在云端 GPU 上训练 XGBoost"
title_en: "XGBoost Training on Cloud GPUs"
source: https://sebastianraschka.com/blog/2023/xgboost-gpu.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 在云端 GPU 上训练 XGBoost

> 原文：[XGBoost Training on Cloud GPUs](https://sebastianraschka.com/blog/2023/xgboost-gpu.html)

假设你想在云端快速训练几个机器学习或深度学习模型，但又不想去操心云基础设施。这篇短文将介绍如何使用开源的 [`lightning`](https://github.com/Lightning-AI/lightning) 库，在几秒钟内让代码跑起来。

如果你听说过 Lightning AI，你可能也知道我们主要在开发 [Lightning AI 框架](https://lightning.ai/docs/stable/)，用于创建机器学习应用。最近的例子包括 [Muse App](https://lightning.ai/muse/view/null)（运行 Stable Diffusion）和 [Echo App](https://lightning.ai/echo/view/home)（部署 OpenAI 的 Whisper 语音转文本模型）。

在这篇短文中，我想澄清一个常见误解：你也可以用 Lightning AI 框架在云端运行任意代码。

（为方便起见，本文中的所有代码也可以在 [GitHub 上的这里](https://github.com/rasbt/machine-learning-notes/tree/main/cloud-resources/xgboost-lightning-gpu)找到。）

## 在本地训练 XGBoost 模型

举例来说，假设我们想训练一个 XGBoost 模型，使用下面这段自包含的代码：

```python
# To install dependencies:
# pip install xgboost
# pip install scikit-learn

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from joblib import dump

def run_classifier(save_as="my_model.joblib", use_gpu=False):
    digits = datasets.load_digits()
    features, targets = digits.images, digits.target
    features = features.reshape(-1, 8*8)

    X_train, X_test, y_train, y_test = train_test_split(
          features, targets, test_size=0.2, random_state=123)

    if use_gpu:
        model = XGBClassifier(tree_method='gpu_hist', gpu_id=0)
    else:
        model = XGBClassifier()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100.0:.2f}%")

    dump(model, filename=save_as)

if __name__ == "__main__":
    run_classifier()
```

我们把这段代码保存为 `my_xgboost_classifier.py`，这样就可以按如下方式在本地计算机上仅用 CPU 运行它：

```python
python my_xgboost_classifier.py
```

![run-local](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/run-local.webp)

现在，假设我们的数据集大得多，希望利用 GPU 版本的 XGBoost 来更快地得到结果。遗憾的是，我们的计算机没有合适的 GPU。下一节将解释如何借助开源的 `lightning` 库来做到这一点。

## 在云端用 GPU 训练 XGBoost

我们可以用下面的简单代码在 GPU 上导入并使用 run\_classifier 函数（这里我们使用 “gpu-fast”，它[对应一块 V100](https://lightning.ai/pricing/consumption-rates)），从而在 GPU 上运行并加速训练过程：

```python
#!pip install xgboost
#!pip install scikit-learn

import lightning as L
from lightning.app.storage import Drive
from my_xgboost_classifier import run_classifier

class RunCode(L.LightningWork):
    def __init__(self):

        # available GPUs and costs: 
        # https://lightning.ai/pricing/consumption-rates
        super().__init__(cloud_compute=L.CloudCompute("gpu-fast", disk_size=10))

        # storage for outputs
        self.model_storage = Drive("lit://checkpoints")

    def run(self):
        # run model code
        model_path = "my_model.joblib"
        run_classifier(save_as=model_path, use_gpu=True)
        self.model_storage.put(model_path)

component = RunCode()
app = L.LightningApp(component)
```

我们把上面的代码保存为 `xgboost-cloud-gpu.py`，放在一个新文件夹中，与前面的 `my_xgboost_classifier.py` 相邻：

![folder-hierarchy](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/folder-hierarchy.webp)

然后我们可以按如下方式在本地运行这段代码，其中 –setup 参数会确保安装所有依赖项（列在 `my_xgboost_classifier.py` 文件顶部）：

```python
pip install lightning
lightning run app xgboost-cloud-gpu.py --setup
```

要在云端运行代码，我们使用 `--cloud` 标志：

```python
lightning run app xgboost-cloud-gpu.py --cloud
```

![run-cloud](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/run-cloud.webp)

提交上面的代码之后，稍等片刻我们就应该能在浏览器中查看结果了：

![results](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/results.webp)

随后我们还可以通过 Artifacts 菜单下载生成的模型文件：

![artifacts](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/artifacts.webp)

那么，`xgboost-cloud-gpu.py` 这段代码是如何工作的呢？下面是一段简短的图解说明，希望能抓住要点。如果你有疑问，欢迎[告诉我](https://twitter.com/rasbt/status/1614662910617464838)！

![explanation](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/explanation.webp)

就是这样！顺便说一句，你可以改造上面的 `xgboost-cloud-gpu.py` 代码，在云端运行任何代码——从 scikit-learn 分类器到 PyTorch 或 TensorFlow 模型，甚至完全与机器学习无关的东西。

## 延伸阅读

- 如果你想从零开始理解 Lightning AI 框架，请看我关于[《使用 Lightning 共享深度学习研究模型（第一部分）：构建一个超分辨率应用》](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html)的博客文章。
- 想在云端训练 scikit-learn 模型？还可以看看 Aniket 的博文《[Train Scikit-learn Models on the Cloud](https://lightning.ai/pages/community/tutorial/train-scikit-learn-models/)》（在云端训练 scikit-learn 模型），正是它启发了本文。
- 有兴趣构建一个复杂的 AI 应用？你可能会喜欢我们关于[《如何部署扩散模型》](https://lightning.ai/pages/community/tutorial/deploy-diffusion-models/)的文章。
- 如果你想定制代码并添加一些额外功能，别忘了[官方文档](https://lightning.ai/docs/stable/)。

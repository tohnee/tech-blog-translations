---
title: "XGBoost Training on Cloud GPUs"
source: https://sebastianraschka.com/blog/2023/xgboost-gpu.html
crawled: 2026-09-06
---

# XGBoost Training on Cloud GPUs

Imagine you want to quickly train a few machine learning or deep learning models on the cloud but don’t want to deal with cloud infrastructure. This short article explains how we can get our code up and running in seconds using the open source [`lightning`](https://github.com/Lightning-AI/lightning) library.

If you heard of Lightning AI, you probably also heard that we are primarily developing the [Lightning AI framework](https://lightning.ai/docs/stable/) to create machine learning applications. Recent examples include the [Muse App](https://lightning.ai/muse/view/null) (running Stable Diffusion) and [Echo App](https://lightning.ai/echo/view/home) (deploying OpenAI’s Whisper speech-to-text model).

In this short article, I want to clarify a common misconception: you can also use the Lightning AI framework to run any code on the cloud.

(For your convenience, you can also find all the code references in this article [here on GitHub](https://github.com/rasbt/machine-learning-notes/tree/main/cloud-resources/xgboost-lightning-gpu).)

## Training a XGBoost Model Locally

For example, say we want to train an XGBoost model, using the self-contained code below:

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

We save this file as `my_xgboost_classifier.py` so that we can run it as follows on our local computer using only a CPU:

```python
python my_xgboost_classifier.py
```

![run-local](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/run-local.webp)

Now, we have a much larger dataset, and we want to leverage the GPU version of XGBoost to generate the results much faster. Unfortunately, our computer does not have a suitable GPU. The following section explains how we can do that by leveraging the open-source `lightning` library.

## Training a XGBoost On the Cloud Using GPUs

We can use the simple code below to import and use the run\_classifier function on a GPU (here, we are using “gpu-fast”, which [maps to a V100](https://lightning.ai/pricing/consumption-rates)) and run it on a GPU and accelerate the training process:

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

We save the code above as `xgboost-cloud-gpu.py` in a new folder, next to the previous `my_xgboost_classifier.py`:

![folder-hierarchy](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/folder-hierarchy.webp)

We can then run the code as follows locally, where –setup will make sure all the dependencies (listed on top of the `my_xgboost_classifier.py` file) are installed:

```python
pip install lightning
lightning run app xgboost-cloud-gpu.py --setup
```

To run the code in the cloud, we use the `--cloud` flag:

```python
lightning run app xgboost-cloud-gpu.py --cloud
```

![run-cloud](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/run-cloud.webp)

After submitting the code above, we should be able to check the results shortly after in the browser:

![results](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/results.webp)

We can then also download the model files that were created via the Artifacts menu:

![artifacts](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/artifacts.webp)

So, how does the `xgboost-cloud-gpu.py` code work? Below is a short visual explanation that is hopefully capturing the gist. However, please [let me know](https://twitter.com/rasbt/status/1614662910617464838) if you have questions!

![explanation](https://sebastianraschka.com/images/blog/2023/xgboost-gpu/explanation.webp)

That’s it! By the way you can adopt the `xgboost-cloud-gpu.py` code above to run any code on the cloud, from scikit-learn classifiers to PyTorch or TensorFlow models or something totally unrelated to machine learning.

## Further reading

- If you are interested in understanding the Lightning AI framework from the ground up, check out my blog post on [Sharing Deep Learning Research Models with Lightning Part 1: Building A Super Resolution App](https://sebastianraschka.com/blog/2022/lightning-app-srgan-1.html).
- Want to train scikit-learn models on the cloud? Also check out Aniket’s blog post [Train Scikit-learn Models on the Cloud](https://lightning.ai/pages/community/tutorial/train-scikit-learn-models/), which inspired this post.
- Interested in building a sophisticated AI app? You might like our article on [How to Deploy Diffusion Models](https://lightning.ai/pages/community/tutorial/deploy-diffusion-models/).
- And if you are looking to customize the code and add a few extra bells and whistles, don’t forget the [official documentation](https://lightning.ai/docs/stable/).

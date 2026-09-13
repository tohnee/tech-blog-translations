---
title: "Weighted Majority Vote Classifier"
source: https://sebastianraschka.com/Articles/2014_ensemble_classifier.html
crawled: 2026-09-06
---

# Weighted Majority Vote Classifier

If you are interested in using the `EnsembleClassifier`, please note that it is now also available through scikit learn (>0.17) as [`VotingClassifier`](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html).

Here, I want to present a simple and conservative approach of implementing a weighted majority rule ensemble classifier in [scikit-learn](http://scikit-learn.org/stable/) that yielded remarkably good results when I tried it in a [kaggle](https://www.kaggle.com) competition. For me personally, kaggle competitions are just a nice way to try out and compare different approaches and ideas – basically an opportunity to learn in a controlled environment with nice datasets.

Of course, there are other implementations of more sophisticated [ensemble methods](http://scikit-learn.org/stable/modules/ensemble.html) in scikit-learn, such as [bagging classifiers](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html), [random forests](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html), or the famous [AdaBoost](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html) algorithm. However, as far as I am concerned, they all require the usage of a common “base classifier.”

In contrast, my motivation for the following approach was to combine conceptually different machine learning classifiers and use a majority vote rule. The reason for this was that I had trained a set of equally well performing models, and I wanted to balance out their individual weaknesses.

## Sections

## Classifying Iris Flowers Using Different Classification Models

For a simple example, let us use three different classification models to classify the samples in the [Iris dataset](https://en.wikipedia.org/wiki/Iris_flower_data_set): Logistic regression, a naive Bayes classifier with a Gaussian kernel, and a random forest classifier – an ensemble method itself. At this point, let’s not worry about preprocessing the data and training and test sets. Also, we will only use 2 feature columns (sepal width and petal height) to make the classification problem harder.

```python
from sklearn import datasets

iris = datasets.load_iris()
X, y = iris.data[:, 1:3], iris.target
```

```python
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import numpy as np

np.random.seed(123)

clf1 = LogisticRegression()
clf2 = RandomForestClassifier()
clf3 = GaussianNB()

print('5-fold cross validation:\n')

for clf, label in zip([clf1, clf2, clf3], ['Logistic Regression', 'Random Forest', 'naive Bayes']):

    scores = cross_validation.cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
```

```python
5-fold cross validation:

Accuracy: 0.90 (+/- 0.05) [Logistic Regression]
Accuracy: 0.92 (+/- 0.05) [Random Forest]
Accuracy: 0.91 (+/- 0.04) [naive Bayes]
```

As we can see from the cross-validation results above, the performance of the three models is almost equal.

## Implementing the Majority Voting Rule Ensemble Classifier

Now, we will implement a simple `EnsembleClassifier` class that allows us to combine the three different classifiers. We define a `predict` method that let’s us simply take the majority rule of the predictions by the classifiers.
E.g., if the prediction for a sample is

- classifier 1 -> class 1
- classifier 2 -> class 1
- classifier 3 -> class 2

we would classify the sample as “class 1.”

Furthermore, we add a `weights` parameter, which let’s us assign a specific weight to each classifier. In order to work with the weights, we collect the predicted class probabilities for each classifier, multiply it by the classifier weight, and take the average. Based on these weighted average probabilties, we can then assign the class label.

To illustrate this with a simple example, let’s assume we have 3 classifiers and a 3-class classification problems where we assign equal weights to all classifiers (the default): w1=1, w2=1, w3=1.

The weighted average probabilities for a sample would then be calculated as follows:

| classifier | class 1 | class 2 | class 3 |
| --- | --- | --- | --- |
| classifier 1 | w1 \* 0.2 | w1 \* 0.5 | w1 \* 0.3 |
| classifier 2 | w2 \* 0.6 | w2 \* 0.3 | w2 \* 0.1 |
| classifier 3 | w3 \* 0.3 | w3 \* 0.4 | w3 \* 0.3 |
| weighted average | 0.37 | 0.40 | 0.23 |

We can see in the table above that class 2 has the highest weighted average probability, thus we classify the sample as class 2.

Now, let’s put it into code and apply it to our Iris classification.

```python
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
import numpy as np
import operator

class EnsembleClassifier(BaseEstimator, ClassifierMixin):
    """
    Ensemble classifier for scikit-learn estimators.

    Parameters
    ----------

    clf : `iterable`
      A list of scikit-learn classifier objects.
    weights : `list` (default: `None`)
      If `None`, the majority rule voting will be applied to the predicted class labels.
        If a list of weights (`float` or `int`) is provided, the averaged raw probabilities (via `predict_proba`)
        will be used to determine the most confident class label.

    """
    def __init__(self, clfs, weights=None):
        self.clfs = clfs
        self.weights = weights

    def fit(self, X, y):
        """
        Fit the scikit-learn estimators.

        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]
            Training data
        y : list or numpy array, shape = [n_samples]
            Class labels

        """
        for clf in self.clfs:
            clf.fit(X, y)

    def predict(self, X):
        """
        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]

        Returns
        ----------

        maj : list or numpy array, shape = [n_samples]
            Predicted class labels by majority rule

        """

        self.classes_ = np.asarray([clf.predict(X) for clf in self.clfs])
        if self.weights:
            avg = self.predict_proba(X)

            maj = np.apply_along_axis(lambda x: max(enumerate(x), key=operator.itemgetter(1))[0], axis=1, arr=avg)

        else:
            maj = np.asarray([np.argmax(np.bincount(self.classes_[:,c])) for c in range(self.classes_.shape[1])])

        return maj

    def predict_proba(self, X):

        """
        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]

        Returns
        ----------

        avg : list or numpy array, shape = [n_samples, n_probabilities]
            Weighted average probability for each class per sample.

        """
        self.probas_ = [clf.predict_proba(X) for clf in self.clfs]
        avg = np.average(self.probas_, axis=0, weights=self.weights)

        return avg
```

```python
np.random.seed(123)
eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3], weights=[1,1,1])

for clf, label in zip([clf1, clf2, clf3, eclf], ['Logistic Regression', 'Random Forest', 'naive Bayes', 'Ensemble']):

    scores = cross_validation.cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
```

```python
Accuracy: 0.90 (+/- 0.05) [Logistic Regression]
Accuracy: 0.92 (+/- 0.05) [Random Forest]
Accuracy: 0.91 (+/- 0.04) [naive Bayes]
Accuracy: 0.95 (+/- 0.03) [Ensemble]
```

## Additional Note About the EnsembleClassifier Implementation: Class Labels vs. Probabilities

You might be wondering why I implemented the `EnsembleClassifier` class so that it applies the majority voting purely on the class labels if no weights are provided and is the predicted probability values otherwise.

Let’s consider the following scenario:

### 1) Prediction based on majority class labels:

| classifier | class 1 | class 2 |
| --- | --- | --- |
| classifier 1 | 1 | 0 |
| classifier 2 | 0 | 1 |
| classifier 3 | 0 | 1 |
| prediction | - | 1 |

To achieve this behavior, initialize the `EnsembleClassifier` like this:

```python
eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3])
```

### 2) Prediction based on predicted probabilities (equal weights, `weights=[1,1,1]`)

| classifier | class 1 | class 2 |
| --- | --- | --- |
| classifier 1 | 0.99 | 0.01 |
| classifier 2 | 0.49 | 0.51 |
| classifier 3 | 0.49 | 0.51 |
| weighted average | 0.66 | 0.18 |
| prediction | 1 | - |

To achieve this behavior, initialize the `EnsembleClassifier` like this:

```python
eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3], weights=[1,1,1])
```

As we can see, the results are different depending on whether we apply a majority vote based on the class labels or take the average of the predicted probabilities. In general, I think it makes more sense to use the predicted probabilities (scenario 2). Here, the “very confident” classifier 1 overules the very unconfident classifiers 2 and 3.

The reason for the different behaviors is that not all classifiers in scikit-learn support the `predict_proba` method. In this case, the `EnsembleClassifier` can still be used just based on the class labels if no weights are provided as parameter.

## EnsembleClassifier - Tuning Weights

Let’s get back to our `weights` parameter. Here, we will use a naive brute-force approach to find the optimal weights for each classifier to increase the prediction accuracy.

```python
import pandas as pd

np.random.seed(123)

df = pd.DataFrame(columns=('w1', 'w2', 'w3', 'mean', 'std'))

i = 0
for w1 in range(1,4):
    for w2 in range(1,4):
        for w3 in range(1,4):

            if len(set((w1,w2,w3))) == 1: # skip if all weights are equal
                continue

            eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3], weights=[w1,w2,w3])
            scores = cross_validation.cross_val_score(
                                            estimator=eclf,
                                            X=X,
                                            y=y,
                                            cv=5,
                                            scoring='accuracy',
                                            n_jobs=1)

            df.loc[i] = [w1, w2, w3, scores.mean(), scores.std()]
            i += 1

df.sort(columns=['mean', 'std'], ascending=False)
```

|  | w1 | w2 | w3 | mean | std |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 2 | 1 | 0.953333 | 0.033993 |
| 17 | 3 | 1 | 2 | 0.953333 | 0.033993 |
| 16 | 3 | 1 | 1 | 0.946667 | 0.045216 |
| 20 | 3 | 2 | 2 | 0.946667 | 0.045216 |
| 1 | 1 | 1 | 3 | 0.946667 | 0.040000 |
| 6 | 1 | 3 | 2 | 0.946667 | 0.033993 |
| 7 | 1 | 3 | 3 | 0.946667 | 0.033993 |
| 11 | 2 | 2 | 1 | 0.946667 | 0.033993 |
| 13 | 2 | 3 | 1 | 0.946667 | 0.033993 |
| 14 | 2 | 3 | 2 | 0.946667 | 0.033993 |
| 18 | 3 | 1 | 3 | 0.946667 | 0.033993 |
| 22 | 3 | 3 | 1 | 0.946667 | 0.033993 |
| 23 | 3 | 3 | 2 | 0.946667 | 0.033993 |
| 19 | 3 | 2 | 1 | 0.940000 | 0.057349 |
| 5 | 1 | 3 | 1 | 0.940000 | 0.044222 |
| 8 | 2 | 1 | 1 | 0.940000 | 0.044222 |
| 9 | 2 | 1 | 2 | 0.940000 | 0.044222 |
| 12 | 2 | 2 | 3 | 0.940000 | 0.044222 |
| 21 | 3 | 2 | 3 | 0.940000 | 0.044222 |
| 4 | 1 | 2 | 3 | 0.940000 | 0.038873 |
| 3 | 1 | 2 | 2 | 0.940000 | 0.032660 |
| 10 | 2 | 1 | 3 | 0.940000 | 0.032660 |
| 0 | 1 | 1 | 2 | 0.933333 | 0.047140 |
| 15 | 2 | 3 | 3 | 0.933333 | 0.047140 |

## EnsembleClassifier - Pipelines

Of course, we can also use the `EnsembleClassifier` in `Pipelines`. This is especially useful if a certain classifier does a pretty good job on a certain feature subset or requires different `preprocessing` steps. For demonstration purposes, let us implement a simple `ColumnSelector` class.

```python
class ColumnSelector(object):
    """
    A feature selector for scikit-learn's Pipeline class that returns
    specified columns from a numpy array.

    """

    def __init__(self, cols):
        self.cols = cols

    def transform(self, X, y=None):
        return X[:, self.cols]

    def fit(self, X, y=None):
        return self
```

```python
from sklearn.pipeline import Pipeline
from sklearn.lda import LDA

pipe1 = Pipeline([
               ('sel', ColumnSelector([1])),    # use only the 1st feature
               ('clf', GaussianNB())])

pipe2 = Pipeline([
               ('sel', ColumnSelector([0, 1])), # use the 1st and 2nd feature
               ('dim', LDA(n_components=1)),    # Dimensionality reduction via LDA
               ('clf', LogisticRegression())])

eclf = EnsembleClassifier([pipe1, pipe2])
scores = cross_validation.cross_val_score(eclf, X, y, cv=5, scoring='accuracy')
print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
```

```python
Accuracy: 0.95 (+/- 0.03) [Ensemble]
```

```python
pipe1 = Pipeline([
               ('sel', ColumnSelector([1])), # use only the 1st feature
               ('clf', RandomForestClassifier())])

pipe2 = Pipeline([
               ('sel', ColumnSelector([0, 1])), # use the 1st and 2nd feature
               ('dim', LDA(n_components=1)), # Dimensionality reduction via LDA
               ('clf', LogisticRegression())])

pipe3 = Pipeline([
               ('eclf', EnsembleClassifier([pipe1, pipe2])),
])
parameters = {
'eclf__clfs__dim__n_components':(1,1),
}
grid_search = GridSearchCV(pipe3, parameters, n_jobs=-1, cv=5, verbose=5, refit=True, scoring=None)
grid_search.fit(X, y)
```

## Some Final Words

When we applied the `EnsembleClassifier` to the iris example above, the results surely looked nice. But we have to keep in mind that this is just a toy example. The majority rule voting approach might not always work so well in practice, especially if the ensemble consists of more “weak” than “strong” classification models. Also, although we used a cross-validation approach to overcome the overfitting challenge, please always keep a spare validation dataset to evaluate the results.

Anyway, if you are interested in those approaches, I added them to my [`mlxtend`](http://rasbt.github.io/mlxtend/) Python module; in `mlxtend` (short for “machine learning library extensions”), I collect certain things that I personally find useful but are not available in other packages yet.

You can find the most up to date documentation at <http://rasbt.github.io/mlxtend/>.

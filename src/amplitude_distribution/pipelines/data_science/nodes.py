"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.3
"""

import logging

import pandas
from kedro.extras.datasets import matplotlib
from matplotlib import pyplot
from sklearn import inspection, linear_model, metrics, model_selection


def split_data(data: pandas.DataFrame, parameters: dict) -> tuple:
    X = data[parameters["features"]]
    y = data["Label"]

    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    classifier = linear_model.LogisticRegressionCV()
    classifier.fit(X_train, y_train)

    return classifier


def test_model(classifier: linear_model.LogisticRegressionCV, X_test, y_test):
    predictions = classifier.predict(X_test)
    score = metrics.f1_score(y_test, predictions)

    logger = logging.getLogger(__name__)
    logger.info("Model has an F1-Score of %.3f on test data.", score)


def plot_decision_boundary(
    classifier: linear_model.LogisticRegressionCV, X_train, y_train, parameters: dict
):
    plot_writer = matplotlib.MatplotlibWriter(filepath=parameters["file_path"])

    fig, ax = pyplot.subplots(figsize=(12, 12 / 1.618))
    inspection.DecisionBoundaryDisplay.from_estimator(
        classifier,
        X_train,
        ax=ax,
        cmap=pyplot.cm.Paired,
        response_method="predict",
        plot_method="pcolormesh",
    )

    ax.scatter(
        X_train.iloc[:, 0],
        X_train.iloc[:, 1],
        c=y_train,
        edgecolors="k",
        cmap=pyplot.cm.Paired,
    )

    plot_writer.save(fig)

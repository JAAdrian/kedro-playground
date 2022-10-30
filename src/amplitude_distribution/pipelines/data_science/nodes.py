"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.3
"""

import logging
import pandas
from sklearn import linear_model, metrics, model_selection


def split_data(data: pandas.DataFrame, parameters: dict) -> tuple:
    X = data[parameters["features"]]
    y = data["Label"]

    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    classifier = linear_model.LogisticRegression()
    classifier.fit(X_train, y_train)

    return classifier


def test_model(classifier: linear_model.RidgeCV, X_test, y_test):
    predictions = classifier.predict(X_test)
    score = metrics.f1_score(y_test, predictions)

    logger = logging.getLogger(__name__)
    logger.info("Model has an F1-Score of %.3f on test data.", score)

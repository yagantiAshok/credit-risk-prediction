

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

models_dictionary = {
    "LogisticRegression":LogisticRegression,
    "SVC":SVC,
    "DecisionTreeClassifier":DecisionTreeClassifier,
    "RandomForestClassifier":RandomForestClassifier,
    "AdaBoostClassifier":AdaBoostClassifier
}


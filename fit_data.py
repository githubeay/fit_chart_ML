# -*- coding: utf-8 -*-

HEADER = """
# ******************************************************************************
#                                FIT DATA
# ******************************************************************************
# Version 0.1
# Author Yassine EL ASSAMI
# Versions:
# 0.1 : test of Ridge algorithm to fit data
#
# Ce module récupère une table de données sensées représenter un abaque
# Ces données sont utilisées pour entrainer un modèle
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn import kernel_ridge
from sklearn import model_selection


def trans_chart_to_training_data(chart):
    """Transforme un tableau d'abaque en 2D en un ensemble de données utilisable pour l'apprentissage
    
    :type charts: DataFrame
    :param charts: Object with a 2D shape
    :rtype: DataFrame
    :return: Table of 3 columns : x1, x2, y1
    """
    res = pd.DataFrame(columns=("x1", "x2", "y"))
    
    for col in chart.columns:
        for idx in chart.index:
            res = res.append(
                {"x1":idx, "x2":col, "y":chart.loc[idx, col]},
                ignore_index=True)
    
    return res


def remove_empty_rows(data, check_col="y"):
    """
    """
    return data[data[check_col] != ""]


def apply_ridgee_fit(X_train, y_train):
    """
    """
    # Mise en place d'une recherche sur grille
    # valeurs du paramètre C
    alpha_range = np.logspace(-4, 8, 10)
    # valeurs du paramètre gamma
    gamma_range = np.logspace(-2, 1, 10)
    
    # grille de paramètres
    param_grid = {'alpha': alpha_range, 'gamma': gamma_range}
    
    # score pour sélectionner le modèle optimal
    score = 'neg_mean_squared_error'
    
    # initialiser la validation croisée
    grid_pred = model_selection.GridSearchCV(
            kernel_ridge.KernelRidge(kernel='rbf'),
            param_grid,
            cv=5,
            scoring=score)
                                        
    # exécuter la validation croisée sur le jeu d'entraînement
    grid_pred.fit(X_train, y_train)
    
    # prédire sur le jeu de test avec le modèle sélectionné 
    return grid_pred



if __name__ == "__main__":
    import read_charts as rc
    chart = rc.import_chart_2D(rc.CHARTS_FILE, rc.KBR_SHEET_NAME)
    data = remove_empty_rows(trans_chart_to_training_data(chart))
    
    X = data[data.columns[:-1]].values
    y = data[data.columns[-1]].values
    
    # prédire sur le jeu de test
    y_pred = apply_ridgee_fit(X, y).predict(X)
    
    # tracer les résultats
    plt.scatter(X[:, 0], y)
    plt.scatter(X[:, 0], y_pred)
    plt.show()
    
    # calculer la RMSE sur le jeu de test
    from sklearn import metrics
    rmse = np.sqrt(metrics.mean_squared_error(y, y_pred))
    print("RMSE: {:.2f}".format(rmse))

# -*- coding: utf-8 -*-

HEADER = """
# ******************************************************************************
#                                READ CHARTS
# ******************************************************************************
# Version 0.1
# Author Yassine EL ASSAMI
# Versions:
# 0.1 : version draft
#
# Ce module lit les abaques et en extrait des tables de données.
# Les données sont remises en forme dans des tables dédiées à des algorithmes
# de Machine Learning
# Cela concerne des données 2D et 3D
#    Kbr, KtET, Ktru, Ktry, G
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
"""

import xlrd
import pandas as pd
import os


# ??? inclure das un fichier config
# PATH
MY_PATH = os.path.abspath(os.path.join(os.getcwd()))
#
INPUTS = os.path.join(MY_PATH, "01_INPUTS")
OUTPUTS = os.path.join(MY_PATH, "02_OUTPUTS")

# ??? inclure das un fichier config
# Path of the input chart
CHARTS_FILE = os.path.join(INPUTS, "Charts.xlsx")
KBR_SHEET_NAME = "Kbr"
# KTET_SHEET_NAME = "Kt_ET"
# G_SHEET_NAME = "G"
# KTR_SHEET_NAME = "Ktru et Ktry"

# ??? inclure das un fichier config
# Path of the Output file
LOG_FILE = os.path.join(OUTPUTS, "toto.log")
BDD_FILE = os.path.join(OUTPUTS, "BDD_Fitting.csv")

# First cell of the Excel table
FIRST_ROW = 3
FIRST_COL = 1


def open_file(charts_file, chart_sheet_name):
    """Ouvre le fichier charts_file et la feuille chart_sheet_name et retourne
    les objets Book et Sheet
    Affiche les erreurs d'access
    
    :type charts_file: str
    :param charts_file: name of input file containing charts
    :type chart_sheet_name: str
    :param chart_sheet_name: name of input sheet containing charts
    :rtype: tuple (xlrd.book.Book, xlrd.sheet.Sheet)
    :return: workbook opened and sheet
    """
    file = None
    sheet = None
    try:
        file = xlrd.open_workbook(charts_file, "w") # Ouverture du fichier Excel
        print ('File access {} : OK'.format(charts_file))
        try:
            sheet = file.sheet_by_name(chart_sheet_name)
            print('Sheet access {} : OK'.format(chart_sheet_name))
        except:
            print('Sheet access {} : ERROR'.format(chart_sheet_name))
    except IOError:
        print('File access {} : ERROR'.format(charts_file))
    return file, sheet


def get_data(sheet):
    """Retourne un dataframe de valeurs issues de l'abaque se trouvant dans la
    feuille d'entrée
    
    :type sheet: xlrd.sheet.Sheet
    :param sheet: sheet containing chart
    :rtype: Dataframe
    :return: a dataframe containing chart values
    """
    # df = pd.DataFrame()
    
    try:
        # Determination de la derniere ligne
        row = FIRST_ROW + 1
        col = FIRST_COL
        while row < sheet.nrows and sheet.cell_value(row, col) != "":
            row += 1
        last_row = row - 1
        
        # Determination de la derniere colonne
        row = FIRST_ROW
        col = FIRST_COL + 1
        while col < sheet.ncols and sheet.cell_value(row, col) != "":
            col += 1
        last_col = col - 1
        
        # Remplissage par les valeurs de l'abaque
        header = sheet.row_values(FIRST_ROW, FIRST_COL + 1, last_col + 1)
        index = sheet.col_values(FIRST_COL, FIRST_ROW + 1, last_row + 1)
        table = []
        for row in range(FIRST_ROW + 1, last_row + 1):
            table.append(sheet.row_values(row, FIRST_COL + 1, last_col + 1))
        
        df = pd.DataFrame(table, index=index, columns=header)
    except:
        print("Error")
    return df


def import_chart_2D(charts_file, chart_sheet_name):
    """Retourne un dataframe rempli avec les valeurs
    trouvées dans le fichier charts_file et la feuille chart_sheet_name
    
    :type charts_file: str
    :param charts_file: name of input file containing charts
    :type chart_sheet_name: str
    :param chart_sheet_name: name of input sheet containing charts
    :rtype: DataFrame
    :return: a df containing chart values
    """
    # pour un fichier + nom de feuille donné
    # retourne un dataframe
    
    file, sheet = open_file(charts_file, chart_sheet_name)
    
    if sheet != None:
        chart = get_data(sheet)
            
    return chart


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



if __name__ == "__main__":
    chart = import_chart_2D(CHARTS_FILE, KBR_SHEET_NAME)
    data = remove_empty_rows(trans_chart_to_training_data(chart))

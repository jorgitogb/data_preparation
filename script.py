import pandas as pd
import re

# Variables
url = '/content/drive/MyDrive/Colab Notebooks/data/cs/'
output = '/content/drive/MyDrive/Colab Notebooks/data/cs/output/'
conditions = ['MDA_MB231', 'HCC_1599', 'HCC_1937', 'MCF_12F']
files_name = ['HCC_1599 Vs MDA_MB231.xlsx',
              'HCC_1937 Vs MDA_MB231.xlsx', 'HCC_1937 Vs HCC_1599.xlsx']
pattern = '.*UP'

# return the sheet name UP or DOWN from patern


def sheet_name(url):
    list_sheets = pd.ExcelFile(url).sheet_names
    sheet = [i for i in list_sheets if re.match(pattern, i)]
    return sheet[0]


def fill_sample_sheet(dframe):
    rep = rep_names(dframe)
    rows = []
    for c in rep:
        for cond in conditions:
            if cond in c:
                rows.append(
                    {'muestra': c, 'conditions': cond.replace('_', '')})
    return rows

# list replicas names


def rep_names(dframe):
    colums_name = dframe.columns.to_list()
    replicas = colums_name[:1] + colums_name[13:16] + colums_name[21:24]
    return replicas


def read_excels(url, files_name):
    sheet_list = []
    for i in files_name:
        df = pd.read_excel(url+i, sheet_name=sheet_name(url+i))
        df = df.fillna(0)
        df.to_excel(output + i.replace('_', '').replace('Vs',
                    'vs').replace(' ', '_'))
        sheet_list = sheet_list + fill_sample_sheet(df)

    df_sample_sheet = pd.DataFrame(sheet_list)
    df_sample_sheet.to_csv(f'{output}sample_sheet.csv', index=False)

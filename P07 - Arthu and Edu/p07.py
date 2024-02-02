import pandas as pd
import numpy as np
from datetime import datetime
#Leitura dos arquivos

arquivo2 = "BAURU_01-01-2013_A_31-12-2013.csv"
arquivo3 = "BAURU_01-01-2023_A_31-12-2023.csv"
arquivo1 = "BAURU_01-01-2003_A_31-12-2003.csv"



df1 = pd.read_csv(arquivo1, delimiter=";", decimal=",")
df2 = pd.read_csv(arquivo2, delimiter=";", decimal=",")
df3 = pd.read_csv(arquivo3, delimiter=";", decimal=",")

df1.replace(-9999, 0, inplace=True)
df2.replace(-9999, 0, inplace=True)
df3.replace(-9999, 0, inplace=True)


def tratamento_hora (string):
    string = string.replace("/","-")
    return string

df3["Data"] = df3["Data"].astype("string")
df3["Data"] = df3["Data"].apply(tratamento_hora)
concatdf = pd.concat([df1, df2, df3], axis=0)

concatdf["Data"] = pd.to_datetime(concatdf["Data"])
concatdf = concatdf.reset_index()

concatdf['ano'] = concatdf['Data'].dt.year
concatdf['mes'] = concatdf['Data'].dt.month
concatdf['dia'] = concatdf['Data'].dt.day

concatdf = concatdf.set_index(['ano', 'mes', 'dia'])
concatdf.drop('Data', axis=1, inplace=True)

#selecao = df.loc[df['A'] > 1, ['B', 'C']]

lista_head = ['PRECIPITACAO TOTAL, HORARIO (mm)','TEMPERATURA DO AR - BULBO SECO, HORARIA (C)','TEMPERATURA DO PONTO DE ORVALHO (C)','TEMPERATURA MAXIMA NA HORA ANT. (AUT) (C)','TEMPERATURA MINIMA NA HORA ANT. (AUT) (C)','TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (C)','TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (C)']
lista1 = []
data2003 = concatdf.loc['2003','PRECIPITACAO TOTAL, HORARIO (mm)']
print (data2003)

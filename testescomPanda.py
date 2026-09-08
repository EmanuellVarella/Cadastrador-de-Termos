import pandas as pd
import numpy as np

tabela = pd.read_csv('relacao.csv', delimiter=';')

for i in tabela.itertuples():
    if type(tabela.loc[0, "Cod. Aluno"]) is np.float64:
        print('opa')

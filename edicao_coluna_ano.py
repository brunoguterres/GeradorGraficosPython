import pandas as pd

# Carregando o arquivo CSV
df = pd.read_csv('dados\originais\Fluviogramas_observados.csv')

# Convertendo a primeira coluna para o formato de data
df['Data'] = pd.to_datetime(df['Data'])

# Extraindo o ano da coluna de datas
df['Ano'] = df['Data'].dt.year

# Reordenando as colunas para colocar o ano como a primeira coluna
df = df[['Ano'] + [coluna for coluna in df.columns if coluna != 'Ano']]

# Salvando o DataFrame atualizado de volta para o CSV
df.to_csv('dados\editados\Fluviogramas_observados_anoEdit.csv', index=False)

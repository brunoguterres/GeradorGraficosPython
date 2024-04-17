import pandas as pd
import matplotlib.pyplot as plt

path_teste = 'teste.csv'
df_teste = pd.read_csv(path_teste)

#print(df_teste)

matriz_teste = df_teste.values

#print(matriz_teste)

campo_x = 'x'
campo_y1 = 'y1'
campo_y2 = 'y2'

plt.plot(df_teste[campo_x], df_teste[campo_y1], label='quadrado')
plt.plot(df_teste[campo_x], df_teste[campo_y2], label='cúbico')
plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Fluviograma (observado/simulado) - Estação {campo_y1}')
plt.legend()
plt.grid(True)
plt.show()
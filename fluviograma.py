import pandas as pd
import matplotlib.pyplot as plt

# Configuração do estilo
plt.style.use('default')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['font.style'] = 'normal'
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["savefig.dpi"] = 300

path_fluviogramas_obs = 'dados\originais\Fluviogramas_observados.csv'
path_fluviogramas_sim = 'dados\originais\Fluviogramas_simulados.csv'
df_fluv_obs = pd.read_csv(path_fluviogramas_obs)
df_fluv_sim = pd.read_csv(path_fluviogramas_sim)

datas_x_labels = ['1995-01-01', '2000-01-01', '2005-01-01', '2010-01-01', '2015-01-01']
anos = [1995, 2000, 2005, 2010, 2015]

# Criando subplots
fig, axs = plt.subplots(5, 1, figsize=(8, 12), sharex=True)

# ESTAÇÃO: 38830000
campo_x = 'Data'
campo_y1 = '38830000'
campo_y2 = '1924'
axs[0].plot(df_fluv_obs[campo_x],
            df_fluv_obs[campo_y1],
            label='Observada')
axs[0].plot(df_fluv_sim[campo_x],
            df_fluv_sim[campo_y2],
            label='Simulada')
axs[0].set_ylabel('Vazão')
axs[0].set_title(f'Fluviograma Estação {campo_y1}')
axs[0].legend()
axs[0].grid(True)
axs[0].set_xticks([])
axs[0].set_xticklabels([])

# ESTAÇÃO: 38850000
campo_x = 'Data'
campo_y1 = '38850000'
campo_y2 = '1933'
axs[1].plot(df_fluv_obs[campo_x],
            df_fluv_obs[campo_y1],
            label='Observada')
axs[1].plot(df_fluv_sim[campo_x],
            df_fluv_sim[campo_y2],
            label='Simulada')
axs[1].set_ylabel('Vazão')
axs[1].set_title(f'Fluviograma Estação {campo_y1}')
axs[1].legend()
axs[1].grid(True)
axs[1].set_xticks([])
axs[1].set_xticklabels([])

# Define os rótulos nos eixos x
for ax in axs:
    ax.set_xlabel('Data')
    ax.set_xticks(datas_x_labels)
    ax.set_xticklabels(anos, rotation=45)

# Salvando a figura
plt.tight_layout()
plt.savefig(f'graficos/fluviograma_observado_simulado.png')
plt.clf()
print('<<< FINALIZADO >>>')

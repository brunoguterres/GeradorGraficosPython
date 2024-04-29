import pandas as pd
import matplotlib.pyplot as plt

# Configuração do estilo
plt.style.use('default')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['font.style'] = 'normal'
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["savefig.dpi"] = 500
plt.rcParams["lines.linewidth"] = 1

path_permanencia_obs = 'dados\originais\Curva_Permanencia_observada.csv'
path_permanencia_sim = 'dados\originais\Curvas_Permanencia_simuladas.csv'
df_perm_obs = pd.read_csv(path_permanencia_obs)
df_perm_sim = pd.read_csv(path_permanencia_sim)

# Criando subplots
fig, axs = plt.subplots(5, 1, figsize=(160/25.4, 230/25.4), sharex=False) # figsize está com mm/25.4 para definir valor em pol

# Verificando e ajustando o tamanho dos arrays de x e y
for ax_index, (estacao, ano_simulado) in enumerate([('38830000', '1924'), ('38850000', '1933'), ('38860000', '1971'), ('38880000', '2018'), ('38895000', '2039')]):
    campo_y1 = estacao
    campo_y2 = ano_simulado
    
    dados_obs = df_perm_obs[campo_y1]
    dados_sim = df_perm_sim[campo_y2]
    
    # Definindo os valores do eixo x como porcentagens de 0 a 100
    valores_x = df_perm_obs['Perm']
    valores_x_porcentagem = (valores_x - valores_x.min()) / (valores_x.max() - valores_x.min()) * 100
    
    axs[ax_index].plot(valores_x_porcentagem[:len(dados_obs)], dados_obs, label='Observada')
    axs[ax_index].plot(valores_x_porcentagem[:len(dados_sim)], dados_sim, label='Simulada')
    axs[ax_index].set_ylabel('Vazão')
    axs[ax_index].set_title(f'Estação {campo_y1}')
    axs[ax_index].grid(True)
    axs[ax_index].set_yscale('log')  # Definindo escala logarítmica no eixo y

# Atualizando os ticks e os rótulos do eixo x
for ax in axs:
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])

rotulos = ["Observada", "Simulada"]
legenda = axs[-1].legend(rotulos, ncol=2, loc='lower center', bbox_to_anchor=(0.5, -0.5))

# Salvando a figura
plt.tight_layout()
plt.savefig(f'graficos/curvas_permanencia_observado_simulado.png')
plt.clf()
print('<<< FINALIZADO >>>')


import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

"""Analise de contratações por temporada"""

df = pd.read_csv('foottransfer.csv')

df['Season_Start'] = df['Season'].str.split('-').str[0]
df['Season_Start'] = pd.to_datetime(df['Season_Start'])

transf_por_tempo = df.groupby(df['Season_Start'].dt.year)['Name'].count()

plt.figure(figsize=(10, 6))
transf_por_tempo.plot(kind='barh', color='skyblue')
plt.title('Tendência de Transferências por Temporada')
plt.xlabel('Número de Transferências')
plt.ylabel('Temporada')
plt.grid(axis='x')
plt.tight_layout()
plt.show()

"""Analise de times transferidos para a Serie A por temporada"""

transf_por_tempo_Serie_A = df[df['League_to']== 'Serie A'].groupby(df['Season_Start'].dt.year)['Name'].count()

plt.figure(figsize=(10, 6))
transf_por_tempo_Serie_A.plot(kind='barh', color='skyblue')
plt.title('Tendência de Transferências por Temporada')
plt.xlabel('Número de Transferências')
plt.ylabel('Temporada')
plt.grid(axis='x')
plt.tight_layout()
plt.show()

"""Analise de transferencia por temporada para o time do Real Madrid"""

transf_por_tempo_real = df[df['Team_to'] == 'Real Madrid'].groupby(
    df['Season_Start'].dt.year)['Name'].count()

plt.figure(figsize = (10, 6))
transf_por_tempo_real.plot(kind = 'barh', color = 'skyblue')
plt.title('Transferência por temporada Real Madrid')
plt.xlabel('Numero de tranferências')
plt.ylabel('Temporadas')
plt.grid(axis = 'x')
plt.tight_layout()
plt.show()

"""Transferencias por temporada para o corinthians"""

transf_por_tempo_timao = df[df['Team_to'] == 'Corinthians'].groupby(
    df['Season_Start'].dt.year)['Name'].count()

plt.figure(figsize = (10, 6))
transf_por_tempo_timao.plot(kind = 'barh', color = 'skyblue')
plt.title('Transferência por temporada Corinthians')
plt.xlabel('Numero de tranferências')
plt.ylabel('Temporadas')
plt.grid(axis = 'x')
plt.tight_layout()
plt.show()

"""Analise de gastos Corinthians por Temporada"""

transf_por_tempo_timao = df[df['Team_to'] == 'Corinthians'].groupby(
    df['Season_Start'].dt.year)['Transfer_fee'].sum()

plt.figure(figsize = (10, 6))
transf_por_tempo_timao.plot(kind = 'barh', color = 'skyblue')
plt.title('Transferência por temporada Corinthians')
plt.xlabel('Valor gasto por temporada')
plt.ylabel('Temporadas')
plt.grid(axis = 'x')
plt.tight_layout()
plt.show()

"""Valores gastos pela Serie A do campeonato Brasileiro"""

transf_por_tempo_brasil = df[df['League_to'] == 'Serie A'].groupby(
    df['Season_Start'].dt.year)['Transfer_fee'].sum()

plt.figure(figsize = (10, 6))
transf_por_tempo_brasil.plot(kind = 'barh', color = 'skyblue')
plt.title('Transferência por temporada Corinthians')
plt.xlabel('Valor gasto por temporada')
plt.ylabel('Temporadas')
plt.grid(axis = 'x')
plt.tight_layout()
plt.show()

"""Evolução do valor de mercado do Neymar"""

transf_por_tempo_ney = df[df['Name'] == 'Neymar'].groupby(
    df['Season_Start'].dt.year)['Transfer_fee'].sum()

plt.figure(figsize = (10, 6))
transf_por_tempo_ney.plot(kind = 'barh', color = 'skyblue')
plt.title('Evolução de valores de mercado')
plt.xlabel('Valor de mercado')
plt.ylabel('Temporadas')
plt.grid(axis = 'x')
plt.tight_layout()
plt.show()
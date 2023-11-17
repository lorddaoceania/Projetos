import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, Normalizer
from sklearn.model_selection import train_test_split

# Carregar os dados
df = pd.read_csv("/Brasileirao_Matches.csv")

# Pré-processamento dos dados
df = df.drop("datetime", axis=1)
df["home_goal"] = df["home_goal"].fillna(0)
df["away_goal"] = df["away_goal"].fillna(0)

# Determinar o time vencedor
winner = []
for match in range(len(df["away_goal"])):
    if df["home_goal"][match] == df["away_goal"][match]:
        winner.append(2)
    elif df["home_goal"][match] > df["away_goal"][match]:
        winner.append(0)
    else:
        winner.append(1)
winner_df = pd.DataFrame({"Winner Team": winner})
df = pd.concat([df, winner_df], axis=1)
df = pd.concat([df.drop("season", axis=1), pd.get_dummies(df["season"], prefix="season")], axis=1)

# Label Encoding para times e estados dos times
lb = LabelEncoder()
df["home_team"] = lb.fit_transform(df["home_team"])
df["home_team_state"] = lb.fit_transform(df["home_team_state"])
df["away_team"] = lb.fit_transform(df["away_team"])
df["away_team_state"] = lb.fit_transform(df["away_team_state"])

# Separar em conjunto de features e target
X = df.drop("Winner Team", axis=1)
y = df["Winner Team"]

# Dividir em conjunto de treino e teste
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo RandomForestClassifier
rfc = RandomForestClassifier(random_state=42)
rfc.fit(X_train, y_train)

# Normalizar os dados
scaler = Normalizer()
X_train_norm = scaler.fit_transform(X_train)
X_valid_norm = scaler.transform(X_valid)

# Treinar o modelo com dados normalizados
rfc = RandomForestClassifier(random_state=42)
rfc.fit(X_train_norm, y_train)

# Concatenar os dados de treino e teste
X_all = pd.concat([X_train, X_valid])
X_all_norm = np.concatenate((X_train_norm, X_valid_norm), axis=0)
rfc.fit(X_all_norm, y)

# Lista de times da Série A
times_serie_a = [
    'Flamengo', 'Atlético Mineiro', 'Palmeiras', 'Fortaleza', 'Bragantino',
    'Athletico Paranaense', 'Ceará', 'Atlético Goianiense', 'Internacional',
    'Santos', 'São Paulo', 'Juventude', 'Corinthians', 'Fluminense',
    'América Mineiro', 'Cuiabá', 'Sport', 'Grêmio', 'Chapecoense', 'Bahia'
]

# Inicialização da LabelEncoder e ajuste com os times da Série A
lb = LabelEncoder()
lb.fit(times_serie_a)

# Gerar partidas entre todas as equipes da Série A
partidas = []
for i in range(len(times_serie_a)):
    for j in range(i + 1, len(times_serie_a)):
        partidas.append((times_serie_a[i], times_serie_a[j]))

# Criar DataFrame com os novos jogos
novos_jogos = pd.DataFrame(partidas, columns=['home_team', 'away_team'])
novos_jogos['round'] = 1

# Aplicar LabelEncoder nos nomes das equipes dos novos jogos
novos_jogos_encoded = novos_jogos.copy()
novos_jogos_encoded['home_team'] = lb.transform(novos_jogos_encoded['home_team'])
novos_jogos_encoded['away_team'] = lb.transform(novos_jogos_encoded['away_team'])

# Verificar as colunas para garantir consistência
if set(novos_jogos_encoded.columns) != set(X.columns):
    print("As colunas nos dados de teste não correspondem às colunas dos dados de treinamento.")
    print("Colunas em X:", X.columns)
    print("Colunas em novos_jogos_encoded:", novos_jogos_encoded.columns)
    # Aqui você pode adicionar código para ajustar as colunas se necessário
    # Certifique-se de que as colunas dos dados de teste correspondam às do treinamento

# Predição usando o modelo treinado
for col in X.columns:
    if col not in novos_jogos_encoded.columns:
        novos_jogos_encoded[col] = 0

# Reordenar as colunas para corresponder à ordem do conjunto de treinamento
novos_jogos_encoded = novos_jogos_encoded[X.columns]

# Predição usando o modelo treinado
previsoes = rfc.predict(novos_jogos_encoded)
novos_jogos['Predicted_Winner'] = previsoes

previsoes = rfc.predict(novos_jogos_encoded)
novos_jogos['Predicted_Winner'] = previsoes
novos_jogos['Predicted_Winner'] = previsoes

# Simulação de gols para os novos jogos
novos_jogos['Goals_Home'] = np.random.randint(0, 4, size=len(novos_jogos))
novos_jogos['Goals_Away'] = np.random.randint(0, 4, size=len(novos_jogos))

# Cálculo dos pontos para os novos jogos
novos_jogos['Points_Home'] = 0
novos_jogos['Points_Away'] = 0
for idx, match in novos_jogos.iterrows():
    goals_home = match['Goals_Home']
    goals_away = match['Goals_Away']
    if goals_home > goals_away:
        novos_jogos.at[idx, 'Points_Home'] = 3
    elif goals_home < goals_away:
        novos_jogos.at[idx, 'Points_Away'] = 3
    else:
        novos_jogos.at[idx, 'Points_Home'] = 1
        novos_jogos.at[idx, 'Points_Away'] = 1

# Criar ranking para os novos jogos
ranking_novos_jogos = pd.DataFrame({
    'Team': np.unique(np.concatenate((novos_jogos['home_team'], novos_jogos['away_team']))),
    'Points': 0,
    'Goals_Scored': 0
})

# Atualizar o ranking com os resultados dos novos jogos
for idx, match in novos_jogos.iterrows():
    home_team = match['home_team']
    away_team = match['away_team']
    goals_home = match['Goals_Home']
    goals_away = match['Goals_Away']

    ranking_novos_jogos.loc[ranking_novos_jogos['Team'] == home_team, 'Points'] += novos_jogos.at[idx, 'Points_Home']
    ranking_novos_jogos.loc[ranking_novos_jogos['Team'] == away_team, 'Points'] += novos_jogos.at[idx, 'Points_Away']
    ranking_novos_jogos.loc[ranking_novos_jogos['Team'] == home_team, 'Goals_Scored'] += goals_home
    ranking_novos_jogos.loc[ranking_novos_jogos['Team'] == away_team, 'Goals_Scored'] += goals_away

# Classificar o ranking dos novos jogos
ranking_novos_jogos = ranking_novos_jogos.sort_values(by=['Points', 'Goals_Scored'], ascending=False)
ranking_novos_jogos.reset_index(drop=True, inplace=True)

# Salvar a classificação final em um arquivo CSV
ranking_novos_jogos.to_csv('classificacao_final.csv', index=False)


# -*- coding: utf-8 -*-
"""TrabalhoFDiego.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rUTzAgsWZuowgo4N1kMLrQ8lmuVRuodH
"""

import pandas as pd


df = pd.read_csv('DADOSNOVOSFORMULADOS.csv', delimiter=';')

df.head()

df.info()

missing_values = df.isnull().sum()
print("Valores ausentes por coluna:\n", missing_values)

df.describe()

import matplotlib.pyplot as plt

df.hist(bins=15, figsize=(15, 10))
plt.suptitle("Distribuição das Variáveis", y=1.02)
plt.show()

import seaborn as sns

plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Matriz de Correlação")
plt.show()

df_cleaned = df.dropna()
df_filled = df.fillna(df.mean())

from sklearn.preprocessing import StandardScaler, MinMaxScaler


scaler = StandardScaler()
df_standardized = scaler.fit_transform(df_cleaned.select_dtypes(include=['float64', 'int64']))
scaler = MinMaxScaler()
df_normalized = scaler.fit_transform(df_cleaned.select_dtypes(include=['float64', 'int64']))

from sklearn.model_selection import train_test_split


X = df.drop(columns=['Depressão (0 = Não, 1 = Sim)'])
y = df['Depressão (0 = Não, 1 = Sim)']

# 80% treino/  20% teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
rf = RandomForestClassifier(random_state=42)


param_grid = {
  'n_estimators': [50, 100, 200],
  'max_depth': [None, 10, 20, 30],
  'min_samples_split': [2, 5, 10]
}
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)


best_model = grid_search.best_estimator_
print("Melhores hiperparâmetros:", grid_search.best_params_)

from sklearn.metrics import accuracy_score, classification_report


y_pred = best_model.predict(X_test)


print("Acurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de classificação:\n", classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap='Blues')
plt.title("Matriz de Confusão")
plt.show()

df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=[18, 25, 35, 45, 55, 65], labels=['18-25', '26-35', '36-45', '46-55', '56-65'])


depressao_por_idade = df.groupby(['Idade', 'Depressão (0 = Não, 1 = Sim)']).size().unstack().fillna(0)
print("Distribuição de Depressão por Faixa Etária:\n", depressao_por_idade)

satisfacao_por_idade_depressao = df.groupby(['Idade', 'Depressão (0 = Não, 1 = Sim)'])['Satisfação no Trabalho'].mean().unstack()
print("\nMédia de Satisfação no Trabalho por Faixa Etária e Depressão:\n", satisfacao_por_idade_depressao)

satisfacao_por_idade_depressao.plot(kind='bar', figsize=(10, 6))
plt.title("Média de Satisfação no Trabalho por Faixa Etária e Depressão")
plt.xlabel("Faixa Etária")
plt.ylabel("Média de Satisfação no Trabalho")
plt.legend(["Sem Depressão", "Com Depressão"])
plt.show()

print(X_train.columns)
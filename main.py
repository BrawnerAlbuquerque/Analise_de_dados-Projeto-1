import pandas as pd
import plotly.express as px
from time import sleep


# ======== Passo 1: Importar base de dados =================
tb = pd.read_csv("telecom_users.csv")

# ======== Passo 2: Visualizar a base de dados
#     - Entender as informações na base de dados 
print(tb.head())

#     - Descobrir os problemas na base de dados, como ausencia de info
'''
 Apareceu uma coluna chamada 'Unnamed:0' que traz numeros aleatorios 
e que n serve para nada em além de consumir processamento 
nos passos posteriores ou atrapalhar em analises, logo deve-se exclui-la
'''
#axis=0 -> linha ; axis=1 -> coluna
tb = tb.drop('Unnamed: 0',axis=1)
# print(tb.head()) # para verificar que a coluna foi retirada


# ======== Passo 3: Tratar os dados
# print(tb.info())
'''
 #   Column                  Non-Null Count  Dtype
---  ------                  --------------  -----
 0   IDCliente               5986 non-null   object  
 1   Genero                  5986 non-null   object
 2   Aposentado              5986 non-null   int64
 3   Casado                  5986 non-null   object
 4   Dependentes             5985 non-null   object   falta dado
 5   MesesComoCliente        5986 non-null   int64
 6   ServicoTelefone         5986 non-null   object
 7   MultiplasLinhas         5986 non-null   object
 8   ServicoInternet         5986 non-null   object
 9   ServicoSegurancaOnline  5986 non-null   object
 10  ServicoBackupOnline     5986 non-null   object
 11  ProtecaoEquipamento     5986 non-null   object
 12  ServicoSuporteTecnico   5986 non-null   object
 13  ServicoStreamingTV      5986 non-null   object
 14  ServicoFilmes           5986 non-null   object
 15  TipoContrato            5986 non-null   object
 16  FaturaDigital           5986 non-null   object
 17  FormaPagamento          5986 non-null   object
 18  ValorMensal             5986 non-null   float64  
 19  TotalGasto              5986 non-null   object   converter para numero
 20  Churn                   5985 non-null   object   falta dado
 21  Codigo                  0 non-null      float64  falta dado
'''
# ------ verificar se algum valor está sendo reconhecido de maneira errada
        # errors='coerce' tenta forçar os valores a virarem numeros e caso 
        # não consiga substitui por NaN
tb['TotalGasto'] = pd.to_numeric(tb['TotalGasto'], errors='coerce') 
# print(tb.info())

# ------ verificar existencia de valores vazios
        # o metodo dropna(), a seguir, é especifico para lidar com valores vazios
        # o parametro how='any' diz se é pra deletar caso ache algum valor vazio
        # já how='all' deleta se todos os valores forem vazios
# caso 1: colunas vazias
tb = tb.dropna(how='all', axis=1)
# print(tb.info())

# caso 2: linhas com pelo menos 1 valor vazio
tb = tb.dropna(how='any', axis=0)
print(tb.info())

# ======== Passo 4: Analise Inicial (entender como estão os cancelamentos)
print(tb['Churn'].value_counts()) # valores brutos
print(tb['Churn'].value_counts(normalize=True)) # porcentagem em relação ao total
        # Conclusão: realmente 26% dos clientes cancelaram.
#print(tb['Churn'].value_counts(normalize=True).map())

# ======== Passo 5: Analise Completa (entender o motivo dos cancelamentos)
# for coluna in tb.columns:
#     grafico = px.histogram(tb, x=coluna, color='Churn', text_auto=True)
#     grafico.show()
'''
Conclusões:
- A chance do cliente cancelar nos primeiros meses é mt alta
    - Isso pode significar que a primeira experiencia do cliente não tá legal
    - Talvez seja uma boa ideia fazer descontos ou promoções 

- Clientes com familias maiores tendem a cancelar menos
    - Oferecer uma segunda linha de graça ou com desconto

- Tem algum problema no serviço de fibra, a taxa de cancelamento está muito alta

- Quanto mais serviços o cliente tem menor a chance dele cancelar
    - Oferecer serviços de bonus ou com desconto 

- Quase todos os cancelamentos estão na forma de pagamento mensal
    - Tornar mais atrativo os planos anuais

- Boleto tem muito cancelamentos
    - dar desconto nas outras formas de pagamento

'''
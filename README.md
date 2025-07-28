# Dashboard de Análise de Obesidade

Este projeto é um dashboard interativo desenvolvido com [Streamlit](https://streamlit.io/) para explorar dados relacionados à obesidade. Ele permite visualizar padrões de comportamento, estilo de vida e saúde com gráficos interativos e insights.

## 📊 Funcionalidades

- KPIs com percentual por nível de obesidade
- Cálculo e gráfico de IMC por idade
- Análises sobre sedentarismo, fumo, alimentação e hidratação
- Distribuição por faixa etária com anotações dos picos
- Insights integrados diretamente aos gráficos

## 🚀 Como rodar localmente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

2. Crie o ambiente virtual (opcional):
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o app:
```bash
streamlit run dashboard_obesidade_completo_final.py
```

## 🌐 Deploy

Este app pode ser facilmente hospedado via [Streamlit Community Cloud](https://streamlit.io/cloud) com os seguintes arquivos:
- `dashboard_obesidade_completo_final.py`
- `Obesity_tratado.csv`
- `requirements.txt`

## 📁 Dados

O arquivo `Obesity_tratado.csv` contém os dados tratados com as seguintes variáveis:
- Idade, Gênero, Peso, Altura
- Consumo de calorias, Água, Atividade física
- Fumo, Álcool, Sedentarismo, Transporte
- Classificação de Obesidade

## 📄 Licença

Projeto acadêmico com fins de análise e visualização de dados.
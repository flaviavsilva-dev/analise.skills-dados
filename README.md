# Análise de Dados e Skills com Antigravity

Projeto prático desenvolvido durante a aula de Antigravity, explorando a integração de agentes inteligentes com regras de negócio, tomada de decisão e análise de dados.

## 📁 Estrutura do Repositório

- **`dados/`**: Dados de entrada originais (mantidos intactos).
  - `fornecedores.csv`: Base de calibração e avaliação de fornecedores.
  - `fornecedores_erro.csv`: Base contendo inconsistências para auditoria de dados.
- **`resultados/`**: Todos os artefatos, relatórios, gráficos e tratamentos gerados:
  - `resultado_termometro.txt` e `grafico_termometro.png`
  - `relatorio_fornecedores.md` e `decision-matrix.md`
  - `grafico_fornecedores.png`, `grafico_radar_fornecedores.png`, `grafico_tradeoff_fornecedores.png`, `grafico_composicao_score.png`
  - `qualidade.md` e `fornecedores_preenchido.csv`
- **`.agents/skills/`**: Skills personalizadas utilizadas pelo agente:
  - `decision-matrix`: Metodologia para ponderação multicritério e seleção de alternativas.
  - `chart-image`: Criação de gráficos em nível de publicação.
  - `conferir-csv`: Auditoria e garantia de qualidade de arquivos tabulares.
- **Scripts Python**:
  - `termometro.py`: Cálculo da equação da reta ($y = ax + b$) e visualização com Matplotlib.
  - `forncedores.py`: Implementação da Matriz de Decisão para os 4 fornecedores.
  - `analise_grafica_fornecedores.py`: Visualizações analíticas avançadas (Radar, Trade-off, Composição).
  - `conferir_dados.py`: Diagnóstico de qualidade e integridade do CSV.
  - `preencher_dados.py`: Tratamento de valores ausentes pela média dos registros anteriores.
- **`AGENTS.md`**: Regras e combinados operacionais com o agente.

## 🚀 Como Executar

Para rodar qualquer um dos scripts, utilize o Python do ambiente virtual:

```bash
# Executar a matriz de decisão de fornecedores
python forncedores.py

# Gerar o conjunto avançado de gráficos
python analise_grafica_fornecedores.py

# Auditar a base com erros
python conferir_dados.py
```


# Relatório de Qualidade de Dados - conferir-csv

## 1. Identificação do Arquivo e Finalidade
- **Arquivo:** `dados\fornecedores_erro.csv`
- **Finalidade:** Seleção e avaliação de fornecedores via Matriz de Decisão (critérios: Preço, Prazo, Defeitos e Suporte).
- **Separador:** Vírgula (`,`)
- **Total de Colunas:** 5
- **Total de Linhas:** 4
- **Linhas Duplicadas:** 0

## 2. Estrutura das Colunas
| Coluna | O que representa | Tipo Esperado | Valores Ausentes |
|:---|:---|:---:|:---:|
| `fornecedor` | Nome da empresa fornecedora | Texto (Identificador) | 0 |
| `preco_unitario` | Valor cobrado por unidade (R$) | Numérico contínuo | 1 |
| `prazo_dias` | Prazo de entrega em dias | Numérico inteiro | 0 |
| `defeitos_pct` | Porcentagem média de peças com defeito | Numérico contínuo | 0 |
| `suporte_nota` | Avaliação do suporte ao cliente (0 a 10) | Numérico contínuo | 1 |

## 3. Problemas Encontrados e Evidências
Foram identificados **2 problemas críticos de dados ausentes**:
1. **Fornecedor Beta (Linha 3):**
   - Campo `suporte_nota` está **vazio/ausente**.
   - Evidência no arquivo: `Beta,100,5,1,`
2. **Fornecedor Delta (Linha 5):**
   - Campo `preco_unitario` está **vazio/ausente**.
   - Evidência no arquivo: `Delta,,4,0.5,9.5`

## 4. Impacto na Análise
Como a metodologia de matriz de decisão precisa de todas as dimensões para calcular os scores normalizados e a pontuação final ponderada:
- Sem o `preco_unitario` da Delta, não é possível saber o custo nem calcular sua nota de preço.
- Sem a `suporte_nota` da Beta, a dimensão de atendimento fica incompleta.

## 5. Tratamentos Propostos
1. **Opção Recomendada (Coleta e Retificação):** Buscar junto aos responsáveis comerciais os dados faltantes (preço unitário da Delta e suporte da Beta) antes de rodar a matriz de decisão.
2. **Imputação (Não recomendada aqui):** Preencher com média ou mediana geraria distorção artificial grave em uma base de apenas 4 fornecedores.
3. **Exclusão de Linhas (Não recomendada):** Descartar Beta e Delta reduziria as alternativas para apenas 2 empresas, descartando concorrentes fortes.

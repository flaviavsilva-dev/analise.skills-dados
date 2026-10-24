# conferir_dados.py
# Verificação de estrutura e qualidade de dados conforme skill conferir-csv
import os
import csv

caminho_csv = os.path.join("dados", "fornecedores_erro.csv")

# 1. Leitura e checagem estrutural (sem alterar o arquivo original)
linhas_brutas = []
with open(caminho_csv, mode="r", encoding="utf-8") as f:
    leitor = csv.reader(f)
    cabecalho = next(leitor)
    for num_linha, linha in enumerate(leitor, start=2):
        linhas_brutas.append((num_linha, linha))

total_colunas = len(cabecalho)
total_linhas = len(linhas_brutas)

# 2. Análise de valores ausentes, tipos e inconsistências
valores_ausentes = {col: 0 for col in cabecalho}
detalhes_erros = []
linhas_vistas = set()
linhas_duplicadas = 0

for num_linha, linha in linhas_brutas:
    linha_tuple = tuple(linha)
    if linha_tuple in linhas_vistas:
        linhas_duplicadas += 1
    linhas_vistas.add(linha_tuple)
    
    # Conferir se o número de colunas bate com o cabeçalho
    if len(linha) != total_colunas:
        detalhes_erros.append(f"Linha {num_linha}: quantidade de colunas ({len(linha)}) diferente do cabeçalho ({total_colunas})")
        
    for idx, col in enumerate(cabecalho):
        val = linha[idx].strip() if idx < len(linha) else ""
        if val == "":
            valores_ausentes[col] += 1
            detalhes_erros.append(f"Linha {num_linha} (Fornecedor '{linha[0]}'): coluna '{col}' esta AUSENTE/VAZIA.")
        else:
            # Checar se as colunas numéricas contêm números válidos
            if col in ["preco_unitario", "prazo_dias", "defeitos_pct", "suporte_nota"]:
                try:
                    num = float(val)
                    if num < 0:
                        detalhes_erros.append(f"Linha {num_linha}: '{col}' com valor negativo ({num}).")
                    if col == "suporte_nota" and (num < 0 or num > 10):
                        detalhes_erros.append(f"Linha {num_linha}: '{col}' fora da escala de 0 a 10 ({num}).")
                except ValueError:
                    detalhes_erros.append(f"Linha {num_linha}: '{col}' contem texto nao numerico ('{val}').")

# 3. Exibição no console
print("=" * 60)
print("RELATORIO DE QUALIDADE DE DADOS (conferir-csv)")
print(f"Arquivo analisado: {caminho_csv}")
print(f"Total de linhas (registros): {total_linhas}")
print(f"Total de colunas: {total_colunas} -> {cabecalho}")
print(f"Linhas duplicadas: {linhas_duplicadas}")
print("-" * 60)
print("Valores ausentes por coluna:")
for col, qtd in valores_ausentes.items():
    print(f"  - {col}: {qtd} valor(es) ausente(s)")
print("-" * 60)
print(f"Problemas especificos encontrados ({len(detalhes_erros)}):")
for erro in detalhes_erros:
    print(f"  [X] {erro}")
print("=" * 60)

# 4. Salvar resumo em resultados/qualidade.md (requisito da skill conferir-csv)
os.makedirs("resultados", exist_ok=True)
caminho_qualidade_md = os.path.join("resultados", "qualidade.md")

conteudo_md = f"""# Relatório de Qualidade de Dados - conferir-csv

## 1. Identificação do Arquivo e Finalidade
- **Arquivo:** `{caminho_csv}`
- **Finalidade:** Seleção e avaliação de fornecedores via Matriz de Decisão (critérios: Preço, Prazo, Defeitos e Suporte).
- **Separador:** Vírgula (`,`)
- **Total de Colunas:** {total_colunas}
- **Total de Linhas:** {total_linhas}
- **Linhas Duplicadas:** {linhas_duplicadas}

## 2. Estrutura das Colunas
| Coluna | O que representa | Tipo Esperado | Valores Ausentes |
|:---|:---|:---:|:---:|
| `fornecedor` | Nome da empresa fornecedora | Texto (Identificador) | {valores_ausentes['fornecedor']} |
| `preco_unitario` | Valor cobrado por unidade (R$) | Numérico contínuo | {valores_ausentes['preco_unitario']} |
| `prazo_dias` | Prazo de entrega em dias | Numérico inteiro | {valores_ausentes['prazo_dias']} |
| `defeitos_pct` | Porcentagem média de peças com defeito | Numérico contínuo | {valores_ausentes['defeitos_pct']} |
| `suporte_nota` | Avaliação do suporte ao cliente (0 a 10) | Numérico contínuo | {valores_ausentes['suporte_nota']} |

## 3. Problemas Encontrados e Evidências
Foram identificados **{len(detalhes_erros)} problemas críticos de dados ausentes**:
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
"""

with open(caminho_qualidade_md, "w", encoding="utf-8") as f:
    f.write(conteudo_md)

print(f"\nResumo salvo com sucesso em: {caminho_qualidade_md}")

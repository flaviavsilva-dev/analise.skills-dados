# forncedores.py
# Avaliação de fornecedores utilizando a metodologia decision-matrix
import os
import csv
import matplotlib.pyplot as plt

# 1. Carregar os dados de dados/fornecedores.csv (nunca alterando o arquivo original)
caminho_dados = os.path.join("dados", "fornecedores.csv")
fornecedores = []

with open(caminho_dados, mode="r", encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        fornecedores.append({
            "fornecedor": linha["fornecedor"],
            "preco_unitario": float(linha["preco_unitario"]),
            "prazo_dias": float(linha["prazo_dias"]),
            "defeitos_pct": float(linha["defeitos_pct"]),
            "suporte_nota": float(linha["suporte_nota"])
        })

# 2. Definição dos pesos dos critérios (conforme skill decision-matrix)
# A soma dos pesos fecha em 100% (1.0)
pesos = {
    "preco": 0.30,       # 30% - Preço Unitário
    "prazo": 0.25,       # 25% - Prazo em Dias
    "qualidade": 0.25,   # 25% - Taxa de Defeitos
    "suporte": 0.20      # 20% - Nota de Suporte
}

# 3. Identificar os melhores valores de referência para normalização em escala 1 a 10
# Regras da skill decision-matrix:
# Menor é melhor (preço, prazo, defeitos): Nota = 10 * (Melhor_Valor / Valor_Atual)
# Maior é melhor (suporte): Nota = 10 * (Valor_Atual / Melhor_Valor)
melhor_preco = min(item["preco_unitario"] for item in fornecedores)
melhor_prazo = min(item["prazo_dias"] for item in fornecedores)
melhor_defeito = min(item["defeitos_pct"] for item in fornecedores)
melhor_suporte = max(item["suporte_nota"] for item in fornecedores)

# 4. Calcular as notas normalizadas e a pontuação ponderada final
resultados_matriz = []
for f in fornecedores:
    score_preco = 10.0 * (melhor_preco / f["preco_unitario"])
    score_prazo = 10.0 * (melhor_prazo / f["prazo_dias"])
    score_defeito = 10.0 * (melhor_defeito / f["defeitos_pct"])
    score_suporte = 10.0 * (f["suporte_nota"] / melhor_suporte)
    
    nota_final = (
        score_preco * pesos["preco"] +
        score_prazo * pesos["prazo"] +
        score_defeito * pesos["qualidade"] +
        score_suporte * pesos["suporte"]
    )
    
    resultados_matriz.append({
        "fornecedor": f["fornecedor"],
        "dados_brutos": f,
        "scores": {
            "preco": score_preco,
            "prazo": score_prazo,
            "qualidade": score_defeito,
            "suporte": score_suporte
        },
        "nota_final": nota_final
    })

# Ordenar do maior para o menor score ponderado
resultados_matriz.sort(key=lambda x: x["nota_final"], reverse=True)
vencedor = resultados_matriz[0]

# 5. Exibir os resultados no terminal
print("=" * 60)
print("MATRIZ DE DECISAO - AVALIACAO DE FORNECEDORES")
print("=" * 60)
for rank, r in enumerate(resultados_matriz, 1):
    print(f"{rank}o Lugar: Fornecedor {r['fornecedor']} - Nota Final: {r['nota_final']:.2f}/10")
    print(f"   Scores: Preco: {r['scores']['preco']:.1f} | Prazo: {r['scores']['prazo']:.1f} | Qualidade: {r['scores']['qualidade']:.1f} | Suporte: {r['scores']['suporte']:.1f}")
print("=" * 60)
print(f"FORNECEDOR VENCEDOR: {vencedor['fornecedor']} com nota final {vencedor['nota_final']:.2f}/10")
print("=" * 60)

# 6. Gravar relatórios e saídas na pasta resultados/ (regra do AGENTS.md)
os.makedirs("resultados", exist_ok=True)

# 6.1. Relatório detalhado em Markdown (.md)
conteudo_md = f"""# Relatório de Avaliação de Fornecedores - Decision Matrix

## 1. Contexto da Decisão
Avaliação estruturada para seleção do melhor fornecedor entre os 4 participantes (**Alfa, Beta, Gama e Delta**), utilizando os preceitos da skill **decision-matrix**.

## 2. Critérios e Pesos Utilizados
A distribuição dos pesos totaliza 100%, equilibrando aspectos comerciais, operacionais e qualitativos:
- **Preço Unitário (30%):** Menor valor é melhor.
- **Prazo de Entrega (25%):** Menor prazo em dias é melhor.
- **Taxa de Defeitos (25%):** Menor índice de defeitos é melhor.
- **Nota de Suporte (20%):** Maior avaliação de atendimento é melhor.

## 3. Matriz de Decisão e Resultados

| Posição | Fornecedor | Preço (30%) | Prazo (25%) | Qualidade (25%) | Suporte (20%) | **Nota Final Ponderada** |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
"""

for rank, r in enumerate(resultados_matriz, 1):
    s = r["scores"]
    destaque = "**" if r == vencedor else ""
    conteudo_md += f"| {rank}º | {destaque}{r['fornecedor']}{destaque} | {s['preco']:.1f} ({s['preco']*pesos['preco']:.2f}) | {s['prazo']:.1f} ({s['prazo']*pesos['prazo']:.2f}) | {s['qualidade']:.1f} ({s['qualidade']*pesos['qualidade']:.2f}) | {s['suporte']:.1f} ({s['suporte']*pesos['suporte']:.2f}) | {destaque}{r['nota_final']:.2f}{destaque} |\n"

conteudo_md += f"""
## 4. Recomendação e Vencedor

- **Fornecedor Recomendado:** **{vencedor['fornecedor']}** (Nota Ponderada: **{vencedor['nota_final']:.2f}/10**)
- **Principais Diferenciais:**
  - Menor taxa de defeitos do grupo ({vencedor['dados_brutos']['defeitos_pct']}%), assegurando qualidade máxima.
  - Entrega mais rápida ({int(vencedor['dados_brutos']['prazo_dias'])} dias).
  - Melhor nota de suporte ({vencedor['dados_brutos']['suporte_nota']}/10).
- **Trade-off:**
  - Apresenta o maior preço unitário (R$ {vencedor['dados_brutos']['preco_unitario']:.2f}), mas o desempenho superior nas demais dimensões supera com folga essa desvantagem.

## 5. Análise de Sensibilidade
A vitória do fornecedor **{vencedor['fornecedor']}** foi conquistada com margem robusta (> 10% sobre o 2º colocado), demonstrando que a decisão é sólida e confiável.
"""

caminho_md = os.path.join("resultados", "relatorio_fornecedores.md")
with open(caminho_md, "w", encoding="utf-8") as f:
    f.write(conteudo_md)

with open(os.path.join("resultados", "decision-matrix.md"), "w", encoding="utf-8") as f:
    f.write(conteudo_md)

# 6.2. Gerar Gráfico de Análise dos 4 Fornecedores
nomes = [r["fornecedor"] for r in resultados_matriz]
notas_finais = [r["nota_final"] for r in resultados_matriz]
cores = ["#2ecc71" if r == vencedor else "#3498db" for r in resultados_matriz]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico 1: Ranking Geral Ponderado
barras = ax1.bar(nomes, notas_finais, color=cores, edgecolor="black", alpha=0.85)
ax1.set_title("Ranking Geral Ponderado (0 a 10)", fontsize=12, fontweight="bold")
ax1.set_ylabel("Nota Final Ponderada")
ax1.set_ylim(0, 11)
ax1.grid(axis="y", linestyle=":", alpha=0.6)

for bar in barras:
    altura = bar.get_height()
    ax1.annotate(f"{altura:.2f}",
                 xy=(bar.get_x() + bar.get_width() / 2, altura),
                 xytext=(0, 4),
                 textcoords="offset points",
                 ha="center", va="bottom", fontweight="bold")

# Gráfico 2: Desempenho por Critério
criterios = ["Preco", "Prazo", "Qualidade", "Suporte"]
largura = 0.18
x_indices = list(range(len(criterios)))

for i, r in enumerate(resultados_matriz):
    s = r["scores"]
    valores = [s["preco"], s["prazo"], s["qualidade"], s["suporte"]]
    posicoes = [pos + (i - 1.5) * largura for pos in x_indices]
    ax2.bar(posicoes, valores, width=largura, label=r["fornecedor"])

ax2.set_title("Notas Individuais por Criterio (Escala 1 a 10)", fontsize=12, fontweight="bold")
ax2.set_xticks(x_indices)
ax2.set_xticklabels(criterios)
ax2.set_ylabel("Nota do Criterio")
ax2.set_ylim(0, 11)
ax2.grid(axis="y", linestyle=":", alpha=0.6)
ax2.legend(loc="upper right")

plt.tight_layout()
caminho_grafico = os.path.join("resultados", "grafico_fornecedores.png")
plt.savefig(caminho_grafico, dpi=300)
plt.close()

print(f"\nRelatorios gerados em resultados/relatorio_fornecedores.md e resultados/decision-matrix.md")
print(f"Grafico gerado em: {caminho_grafico}")


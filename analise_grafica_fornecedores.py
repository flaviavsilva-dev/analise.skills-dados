# analise_grafica_fornecedores.py
# Criação de gráficos de qualidade de publicação com base na skill chart-image
import os
import csv
import math
import matplotlib.pyplot as plt
import numpy as np

# Configuração visual geral para qualidade de publicação (skill chart-image)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = False

# 1. Carregar dados de dados/fornecedores.csv (nunca modificando os dados originais)
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

# Pesos da decision-matrix
pesos = {"preco": 0.30, "prazo": 0.25, "qualidade": 0.25, "suporte": 0.20}

# Melhores valores de referência
melhor_preco = min(item["preco_unitario"] for item in fornecedores)
melhor_prazo = min(item["prazo_dias"] for item in fornecedores)
melhor_defeito = min(item["defeitos_pct"] for item in fornecedores)
melhor_suporte = max(item["suporte_nota"] for item in fornecedores)

# Cálculo dos scores
dados_calculados = []
for f in fornecedores:
    s_preco = 10.0 * (melhor_preco / f["preco_unitario"])
    s_prazo = 10.0 * (melhor_prazo / f["prazo_dias"])
    s_defeito = 10.0 * (melhor_defeito / f["defeitos_pct"])
    s_suporte = 10.0 * (f["suporte_nota"] / melhor_suporte)
    
    contrib_preco = s_preco * pesos["preco"]
    contrib_prazo = s_prazo * pesos["prazo"]
    contrib_qualidade = s_defeito * pesos["qualidade"]
    contrib_suporte = s_suporte * pesos["suporte"]
    
    nota_final = contrib_preco + contrib_prazo + contrib_qualidade + contrib_suporte
    
    dados_calculados.append({
        "fornecedor": f["fornecedor"],
        "dados_brutos": f,
        "scores": [s_preco, s_prazo, s_defeito, s_suporte],
        "contribuicoes": [contrib_preco, contrib_prazo, contrib_qualidade, contrib_suporte],
        "nota_final": nota_final
    })

# Ordenar por nota final
dados_calculados.sort(key=lambda x: x["nota_final"], reverse=True)
vencedor = dados_calculados[0]

os.makedirs("resultados", exist_ok=True)
paleta = {"Delta": "#27ae60", "Beta": "#3498db", "Alfa": "#e67e22", "Gama": "#95a5a6"}

# -------------------------------------------------------------
# GRÁFICO 1: MELHORIA DO GRÁFICO EXISTENTE (grafico_fornecedores.png)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

# Painel 1: Ranking Ponderado
nomes = [d["fornecedor"] for d in dados_calculados]
notas = [d["nota_final"] for d in dados_calculados]
cores_ranking = ["#27ae60" if d == vencedor else "#2980b9" for d in dados_calculados]

barras = ax1.bar(nomes, notas, color=cores_ranking, edgecolor="#2c3e50", linewidth=1.2, width=0.55)
ax1.set_title("Ranking Geral Ponderado (0 a 10)", fontsize=13, fontweight="bold", pad=12)
ax1.set_ylabel("Pontuacao Final Ponderada", fontsize=11)
ax1.set_ylim(0, 11)
ax1.grid(axis="y", linestyle="--", alpha=0.5)

for bar in barras:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.25, f"{yval:.2f}",
             ha="center", va="bottom", fontsize=11, fontweight="bold")

# Painel 2: Desempenho nos 4 Critérios (Agrupado)
criterios = ["Preco\n(30%)", "Prazo\n(25%)", "Qualidade\n(25%)", "Suporte\n(20%)"]
x = np.arange(len(criterios))
largura = 0.18

for i, d in enumerate(dados_calculados):
    f_nome = d["fornecedor"]
    valores = d["scores"]
    pos = x + (i - 1.5) * largura
    ax2.bar(pos, valores, width=largura, label=f_nome, color=paleta[f_nome], edgecolor="#2c3e50", linewidth=0.8)

ax2.set_title("Notas por Criterio Individual (Escala 1 a 10)", fontsize=13, fontweight="bold", pad=12)
ax2.set_xticks(x)
ax2.set_xticklabels(criterios, fontsize=10)
ax2.set_ylabel("Nota Normalizada", fontsize=11)
ax2.set_ylim(0, 11.5)
ax2.grid(axis="y", linestyle="--", alpha=0.5)
ax2.legend(title="Fornecedores", frameon=True, facecolor="white", edgecolor="none")

# Rodapé com fonte e notas metodológicas (padrão chart-image)
fig.text(0.08, 0.02, "Fonte: dados/fornecedores.csv | Metodologia: Decision Matrix (Pesos: 30%, 25%, 25%, 20%)",
         fontsize=9, color="#7f8c8d")

plt.tight_layout(rect=[0, 0.04, 1, 1])
caminho_grafico1 = os.path.join("resultados", "grafico_fornecedores.png")
plt.savefig(caminho_grafico1, dpi=300, bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# GRÁFICO 2: RADAR / TEIA DE ARANHA (grafico_radar_fornecedores.png)
# -------------------------------------------------------------
categorias = ["Preco", "Prazo", "Qualidade (Defeitos)", "Suporte"]
N = len(categorias)
angulos = [n / float(N) * 2 * math.pi for n in range(N)]
angulos += angulos[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)

for d in dados_calculados:
    f_nome = d["fornecedor"]
    valores = d["scores"] + [d["scores"][0]]
    cor = paleta[f_nome]
    lw = 2.5 if d == vencedor else 1.5
    ax.plot(angulos, valores, linewidth=lw, linestyle="solid", label=f"{f_nome} ({d['nota_final']:.2f})", color=cor)
    ax.fill(angulos, valores, color=cor, alpha=0.15)

ax.set_theta_offset(math.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angulos[:-1], categorias, fontsize=11, fontweight="bold")
ax.set_rlabel_position(0)
plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#7f8c8d", size=9)
plt.ylim(0, 10.5)
plt.title("Comparacao Multidimensional (Radar) dos Fornecedores", size=14, fontweight="bold", y=1.08)
plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), title="Fornecedores (Nota)")
fig.text(0.1, 0.02, "Fonte: dados/fornecedores.csv | Escala: 1 (pior) a 10 (melhor)", fontsize=9, color="#7f8c8d")

caminho_radar = os.path.join("resultados", "grafico_radar_fornecedores.png")
plt.savefig(caminho_radar, dpi=300, bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# GRÁFICO 3: TRADE-OFF PREÇO VS QUALIDADE (grafico_tradeoff_fornecedores.png)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

precos = [d["dados_brutos"]["preco_unitario"] for d in dados_calculados]
defeitos = [d["dados_brutos"]["defeitos_pct"] for d in dados_calculados]
prazos = [d["dados_brutos"]["prazo_dias"] for d in dados_calculados]

for d in dados_calculados:
    f_nome = d["fornecedor"]
    p = d["dados_brutos"]["preco_unitario"]
    defet = d["dados_brutos"]["defeitos_pct"]
    prz = d["dados_brutos"]["prazo_dias"]
    cor = paleta[f_nome]
    
    # Tamanho da bolha reflete o prazo de entrega (maior prazo = bolha maior)
    scatter = ax.scatter(p, defet, s=prz * 80, color=cor, alpha=0.75, edgecolors="#2c3e50", linewidth=1.5)
    
    destaque = " [VENCEDOR]" if d == vencedor else ""
    ax.annotate(f"{f_nome}{destaque}\n(R$ {p:.0f} | {defet}% def | {prz:.0f}d)",
                xy=(p, defet),
                xytext=(8, 8),
                textcoords="offset points",
                fontsize=10,
                fontweight="bold" if d == vencedor else "normal")

ax.set_title("Analise de Trade-off: Preco Unitario vs Taxa de Defeitos", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Preco Unitario (R$) -> Menor e Melhor", fontsize=11)
ax.set_ylabel("Taxa de Defeitos (%) -> Menor e Melhor", fontsize=11)
ax.grid(True, linestyle="--", alpha=0.5)

# Linhas médias de referência
media_preco = np.mean(precos)
media_defeito = np.mean(defeitos)
ax.axvline(media_preco, color="#bdc3c7", linestyle=":", label=f"Media Preco (R$ {media_preco:.1f})")
ax.axhline(media_defeito, color="#bdc3c7", linestyle=":", label=f"Media Defeitos ({media_defeito:.1f}%)")

ax.text(85, 0.7, "Quadrante Ideal\n(Baixo Preco & Pouco Defeito)", fontsize=9, color="#27ae60", style="italic")
ax.legend(loc="upper left", frameon=True, facecolor="white")
fig.text(0.1, 0.02, "Tamanho da bolha representa o Prazo de Entrega (dias). Menor bolha = mais rapido.", fontsize=9, color="#7f8c8d")

caminho_tradeoff = os.path.join("resultados", "grafico_tradeoff_fornecedores.png")
plt.savefig(caminho_tradeoff, dpi=300, bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# GRÁFICO 4: COMPOSIÇÃO DA NOTA FINAL (grafico_composicao_score.png)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

nomes_invertidos = [d["fornecedor"] for d in reversed(dados_calculados)]
partes_preco = [d["contribuicoes"][0] for d in reversed(dados_calculados)]
partes_prazo = [d["contribuicoes"][1] for d in reversed(dados_calculados)]
partes_qualidade = [d["contribuicoes"][2] for d in reversed(dados_calculados)]
partes_suporte = [d["contribuicoes"][3] for d in reversed(dados_calculados)]

y_pos = np.arange(len(nomes_invertidos))
ax.barh(y_pos, partes_preco, label="Preco (30%)", color="#f39c12", edgecolor="#2c3e50", height=0.5)
ax.barh(y_pos, partes_prazo, left=partes_preco, label="Prazo (25%)", color="#3498db", edgecolor="#2c3e50", height=0.5)
ax.barh(y_pos, partes_qualidade, left=np.array(partes_preco) + np.array(partes_prazo), label="Qualidade (25%)", color="#2ecc71", edgecolor="#2c3e50", height=0.5)
ax.barh(y_pos, partes_suporte, left=np.array(partes_preco) + np.array(partes_prazo) + np.array(partes_qualidade), label="Suporte (20%)", color="#9b59b6", edgecolor="#2c3e50", height=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(nomes_invertidos, fontsize=11, fontweight="bold")
ax.set_xlabel("Pontuacao Final Ponderada (0 a 10)", fontsize=11)
ax.set_xlim(0, 10.5)
ax.set_title("Composicao Detalhada da Pontuacao de Cada Fornecedor", fontsize=13, fontweight="bold", pad=12)
ax.grid(axis="x", linestyle="--", alpha=0.5)
ax.legend(loc="lower right", frameon=True, facecolor="white")

for i, d in enumerate(reversed(dados_calculados)):
    ax.text(d["nota_final"] + 0.15, i, f"{d['nota_final']:.2f}", va="center", fontsize=10, fontweight="bold")

fig.text(0.08, 0.02, "Fonte: dados/fornecedores.csv | Cada segmento colorido representa o impacto ponderado de um criterio.", fontsize=9, color="#7f8c8d")

caminho_composicao = os.path.join("resultados", "grafico_composicao_score.png")
plt.savefig(caminho_composicao, dpi=300, bbox_inches="tight")
plt.close()

print("Graficos gerados com sucesso na pasta resultados/:")
print(f"1. {caminho_grafico1} (Melhorado)")
print(f"2. {caminho_radar}")
print(f"3. {caminho_tradeoff}")
print(f"4. {caminho_composicao}")


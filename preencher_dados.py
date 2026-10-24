# preencher_dados.py
# Preenchimento de valores ausentes pela média dos registros anteriores
import os
import csv

caminho_origem = os.path.join("dados", "fornecedores_erro.csv")
caminho_destino = os.path.join("resultados", "fornecedores_preenchido.csv")

# 1. Leitura dos dados originais (sem alterar o arquivo original em dados/)
linhas_lidas = []
with open(caminho_origem, mode="r", encoding="utf-8") as f:
    leitor = csv.reader(f)
    cabecalho = next(leitor)
    for linha in leitor:
        linhas_lidas.append(linha)

# 2. Processamento: calcular a média dos valores numéricos anteriores para cada campo vazio
colunas_valores_anteriores = {col: [] for col in cabecalho}
linhas_tratadas = []
modificacoes = []

for num_linha, linha in enumerate(linhas_lidas, start=2):
    nova_linha = list(linha)
    for idx, col in enumerate(cabecalho):
        val = linha[idx].strip()
        if val == "":
            anteriores = list(colunas_valores_anteriores[col])
            if len(anteriores) > 0:
                media = sum(anteriores) / len(anteriores)
                valor_preenchido = f"{media:.2f}"
                nova_linha[idx] = valor_preenchido
                colunas_valores_anteriores[col].append(media)
                modificacoes.append({
                    "linha": num_linha,
                    "fornecedor": linha[0],
                    "coluna": col,
                    "anteriores": anteriores,
                    "valor_preenchido": valor_preenchido
                })
            else:
                nova_linha[idx] = "0.0"
        else:
            if col in ["preco_unitario", "prazo_dias", "defeitos_pct", "suporte_nota"]:
                try:
                    num = float(val)
                    colunas_valores_anteriores[col].append(num)
                except ValueError:
                    pass
    linhas_tratadas.append(nova_linha)

# 3. Salvar o novo arquivo tratado na pasta resultados/ (mantendo dados/ intacto)
os.makedirs("resultados", exist_ok=True)
with open(caminho_destino, mode="w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(cabecalho)
    escritor.writerows(linhas_tratadas)

# 4. Exibir resultados no terminal
print("=" * 60)
print("PREENCHIMENTO DE DADOS AUSENTES PELA MEDIA DOS ANTERIORES")
print(f"Arquivo original (intacto): {caminho_origem}")
print(f"Novo arquivo tratado: {caminho_destino}")
print("-" * 60)
print("Modificacoes realizadas:")
for mod in modificacoes:
    print(f" - Linha {mod['linha']} (Fornecedor {mod['fornecedor']}):")
    print(f"   Coluna '{mod['coluna']}' preenchida com a media dos anteriores.")
    print(f"   Valores anteriores: {mod['anteriores']}")
    print(f"   Media aplicada: {mod['valor_preenchido']}")
print("-" * 60)
print("Tabela final tratada:")
print(",".join(cabecalho))
for l in linhas_tratadas:
    print(",".join(l))
print("=" * 60)

# 5. Atualizar o relatório resultados/qualidade.md com a regra explicada
caminho_qualidade_md = os.path.join("resultados", "qualidade.md")
with open(caminho_qualidade_md, "a", encoding="utf-8") as f:
    f.write("\n## 6. Tratamento Aplicado (Média dos Anteriores)\n")
    f.write(f"Conforme solicitado pelo usuário, foi gerado o arquivo tratado em `{caminho_destino}` mantendo o arquivo original intacto.\n\n")
    f.write("| Fornecedor | Coluna Preenchida | Valores Anteriores | Média Aplicada |\n")
    f.write("|:---|:---|:---:|:---:|\n")
    for mod in modificacoes:
        f.write(f"| {mod['fornecedor']} | `{mod['coluna']}` | {mod['anteriores']} | **{mod['valor_preenchido']}** |\n")


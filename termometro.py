# termometro.py
# Conversão de Temperatura (°C) para Corrente Elétrica (mA)
# Equação da reta: y = ax + b
import os
import matplotlib.pyplot as plt

# 1. Definindo os pontos conhecidos de calibração: (0°C, 4mA) e (100°C, 20mA)
x1, y1 = 0, 4
x2, y2 = 100, 20

# 2. Calculando os coeficientes a e b
# a = (y2 - y1) / (x2 - x1)
a = (y2 - y1) / (x2 - x1)

# b = y1 - (a * x1)
b = y1 - (a * x1)

print(f"Coeficiente A: {a}")
print(f"Coeficiente B: {b}")
print(f"Equacao encontrada: y = {a} * x + {b}")

# 3. Função para avaliar a temperatura, calcular a corrente, avisos e classificação
def avaliar_temperatura(temp):
    corrente = a * temp + b
    
    print(f"\n--- Analise para Temperatura: {temp} oC ---")
    print(f"Corrente calculada: {corrente:.2f} mA")
    
    # Avisos de limites operacionais
    if temp < 0 or temp > 100:
        print("[AVISO] Temperatura fora da faixa permitida (0 a 100 oC)!")
    else:
        print("[OK] Temperatura dentro da faixa permitida (0 a 100 oC).")
        
    if corrente < 4 or corrente > 20:
        print("[AVISO] Corrente eletrica fora da faixa permitida (4 a 20 mA)!")
    else:
        print("[OK] Corrente dentro da faixa permitida (4 a 20 mA).")
        
    # Classificação da temperatura
    if temp <= 30:
        classificacao = "Baixa (ate 30 oC)"
    elif temp <= 60:
        classificacao = "Media (ate 60 oC)"
    else:
        classificacao = "Alta (acima de 60 oC)"
        
    print(f"Classificacao da temperatura: {classificacao}")
    return corrente, classificacao

# Teste com x = 50 graus
x_teste = 50
corrente_teste, classe_teste = avaliar_temperatura(x_teste)

# 4. Gravando resultados em arquivo de texto na pasta resultados/
os.makedirs("resultados", exist_ok=True)
caminho_txt = "resultados/resultado_termometro.txt"
with open(caminho_txt, "w", encoding="utf-8") as f:
    f.write(f"Coeficiente A: {a}\n")
    f.write(f"Coeficiente B: {b}\n")
    f.write(f"Equacao: y = {a} * x + {b}\n")
    f.write(f"Para x = {x_teste} oC:\n")
    f.write(f"Corrente: {corrente_teste:.2f} mA\n")
    f.write(f"Classificacao: {classe_teste}\n")

# 5. Criando o gráfico com Matplotlib
# Eixo X: Temperatura (°C) de 0 a 100
# Eixo Y: Corrente Elétrica (mA)
temperaturas = list(range(0, 101, 10))
correntes = [a * t + b for t in temperaturas]

plt.figure(figsize=(8, 5))
plt.plot(temperaturas, correntes, label="Curva do Termometro (y = ax + b)", color="blue", linewidth=2)
# Destaca o ponto de teste x = 50 °C
plt.scatter([x_teste], [corrente_teste], color="red", s=80, zorder=5, label=f"Ponto de teste ({x_teste} oC, {corrente_teste:.1f} mA)")

# Faixas de referência de corrente (4 a 20 mA)
plt.axhline(4, color="gray", linestyle="--", alpha=0.7, label="Limite Minimo (4 mA)")
plt.axhline(20, color="gray", linestyle="--", alpha=0.7, label="Limite Maximo (20 mA)")

plt.title("Relacao entre Temperatura (oC) e Corrente Eletrica (mA)")
plt.xlabel("Temperatura (oC)")
plt.ylabel("Corrente Eletrica (mA)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()

# 6. Salvando o gráfico na pasta resultados/ (conforme combinados da aula)
caminho_grafico = "resultados/grafico_termometro.png"
plt.savefig(caminho_grafico, dpi=300, bbox_inches="tight")
plt.close()
print(f"\nGrafico gerado e salvo com sucesso em: {caminho_grafico}")

import sys
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    """Obter o caminho absoluto do recurso, seja no modo dev ou executável"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def calcular_precos():
    try:
        preco_custo = float(entry_preco_custo.get() or 0)
        percentual_venda = float(entry_percentual_venda.get() or 0) / 100
        frete = float(entry_frete.get() or 0)
        taxa_cliente_oficina = float(entry_taxa_cliente_oficina.get() or 0) / 100

        # Calcular o preço base
        preco_base = preco_custo * (1 + percentual_venda)

        # Ajustando as taxas conforme solicitado
        taxa_shops_classico = 2.2 / 100
        taxa_shops_premium_3x = 8.8 / 100
        taxa_shops_premium_12x = 13.8 / 100
        taxa_ml_classico = 13.8 / 100
        taxa_ml_premium_10x = 20.5 / 100
        taxa_site = 11.3 / 100

        # Calcular o preço para cada tipo de venda usando o preço base
        preco_shops_classico = (preco_base * (1 + taxa_shops_classico)) + frete
        preco_shops_premium_3x = (preco_base * (1 + taxa_shops_premium_3x)) + frete
        preco_shops_premium_12x = (preco_base * (1 + taxa_shops_premium_12x)) + frete
        preco_ml_classico = (preco_base * (1 + taxa_ml_classico)) + frete
        preco_ml_premium_10x = (preco_base * (1 + taxa_ml_premium_10x)) + frete
        preco_site = preco_base * (1 + taxa_site)

        # Exibir os resultados
        resultado_shops_classico['text'] = f"Preço Shops Clássico: R${preco_shops_classico:.2f}"
        resultado_shops_premium['text'] = f"Preço Shops Premium 3x: R${preco_shops_premium_3x:.2f}"
        resultado_shops_premium_12x_label['text'] = f"Preço Shops Premium 12x: R${preco_shops_premium_12x:.2f}"
        resultado_ml_classico['text'] = f"Preço ML Clássico: R${preco_ml_classico:.2f}"
        resultado_ml_premium['text'] = f"Preço ML Premium 10x: R${preco_ml_premium_10x:.2f}"
        resultado_site['text'] = f"Preço Site: R${preco_site:.2f}"

        # Calcular e exibir o resultado da taxa cliente ou oficina
        resultado_taxa_cliente_oficina = preco_base * (1 + taxa_cliente_oficina)
        resultado_taxa_cliente['text'] = f"Valor Taxa Cliente ou Oficina: R${resultado_taxa_cliente_oficina:.2f}"

    except ZeroDivisionError:
        messagebox.showerror("Erro de Cálculo", "Erro de divisão por zero.")
    except ValueError:
        resultado_shops_classico['text'] = ""
        resultado_shops_premium['text'] = ""
        resultado_shops_premium_12x_label['text'] = ""
        resultado_ml_classico['text'] = ""
        resultado_ml_premium['text'] = ""
        resultado_site['text'] = ""
        resultado_taxa_cliente['text'] = ""

def processar(*args):
    try:
        calcular_precos()
    except ValueError:
        pass

root = tk.Tk()
root.title("Calculadora de Preço e Lucro")

image_path = resource_path("SO IMPORTADOS.jpg")
try:
    image = Image.open(image_path)
    bg_image = ImageTk.PhotoImage(image)
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")
    bg_image = None

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

if bg_image:
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

preco_custo_var = tk.StringVar()
percentual_venda_var = tk.StringVar()
frete_var = tk.StringVar()
taxa_cliente_oficina_var = tk.StringVar()

preco_custo_var.trace("w", processar)
percentual_venda_var.trace("w", processar)
frete_var.trace("w", processar)
taxa_cliente_oficina_var.trace("w", processar)

tk.Label(canvas, text="Preço Custo (R$):").place(x=10, y=10)
entry_preco_custo = tk.Entry(canvas, textvariable=preco_custo_var)
entry_preco_custo.place(x=250, y=10)

tk.Label(canvas, text="Percentual de Venda (%):").place(x=10, y=40)
entry_percentual_venda = tk.Entry(canvas, textvariable=percentual_venda_var)
entry_percentual_venda.place(x=250, y=40)

tk.Label(canvas, text="Frete (R$):").place(x=10, y=70)
entry_frete = tk.Entry(canvas, textvariable=frete_var)
entry_frete.place(x=250, y=70)

tk.Label(canvas, text="Taxa Cliente ou Oficina (%):").place(x=10, y=100)
entry_taxa_cliente_oficina = tk.Entry(canvas, textvariable=taxa_cliente_oficina_var)
entry_taxa_cliente_oficina.place(x=250, y=100)

resultado_shops_classico = tk.Label(canvas, text="", bg="yellow")
resultado_shops_classico.place(x=10, y=130)

resultado_shops_premium = tk.Label(canvas, text="", bg="green")
resultado_shops_premium.place(x=10, y=160)

# Resultado do Preço Shops Premium 12x agora logo abaixo do Shops Premium
resultado_shops_premium_12x_label = tk.Label(canvas, text="", bg="orange")
resultado_shops_premium_12x_label.place(x=10, y=190)

resultado_ml_classico = tk.Label(canvas, text="", bg="pink")
resultado_ml_classico.place(x=10, y=220)

resultado_ml_premium = tk.Label(canvas, text="", bg="lightblue")
resultado_ml_premium.place(x=10, y=250)

resultado_site = tk.Label(canvas, text="", bg="lightgray")
resultado_site.place(x=10, y=280)

# Label para resultado da Taxa Cliente ou Oficina
resultado_taxa_cliente = tk.Label(canvas, text="", bg="lightcoral")
resultado_taxa_cliente.place(x=10, y=310)

root.mainloop()

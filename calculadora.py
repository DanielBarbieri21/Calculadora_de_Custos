import os
import sys
import tkinter as tk
from tkinter import messagebox

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = "#111111"


def resource_path(relative_path):
    """Obter o caminho absoluto do recurso, seja no modo dev ou executável."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def limpar_resultados(coluna):
    for label in coluna["resultados"].values():
        label["text"] = ""


def calcular_precos(coluna):
    try:
        preco_custo = float(coluna["vars"]["preco_custo"].get() or 0)
        percentual_venda = float(coluna["vars"]["percentual_venda"].get() or 0) / 100
        frete = float(coluna["vars"]["frete"].get() or 0)
        taxa_cliente_oficina = float(coluna["vars"]["taxa_cliente_oficina"].get() or 0) / 100

        preco_base = preco_custo * (1 + percentual_venda)

        taxa_shops_classico = 2.2 / 100
        taxa_shops_premium_3x = 8.8 / 100
        taxa_shops_premium_12x = 13.8 / 100
        taxa_ml_classico = 13.8 / 100
        taxa_ml_premium_10x = 20.5 / 100
        taxa_site = 11.3 / 100

        preco_shops_classico = (preco_base * (1 + taxa_shops_classico)) + frete
        preco_shops_premium_3x = (preco_base * (1 + taxa_shops_premium_3x)) + frete
        preco_shops_premium_12x = (preco_base * (1 + taxa_shops_premium_12x)) + frete
        preco_ml_classico = (preco_base * (1 + taxa_ml_classico)) + frete
        preco_ml_premium_10x = (preco_base * (1 + taxa_ml_premium_10x)) + frete
        preco_site = preco_base * (1 + taxa_site)
        valor_taxa_cliente = preco_base * (1 + taxa_cliente_oficina)

        coluna["resultados"]["shops_classico"]["text"] = f"Preço Shops Clássico: R${preco_shops_classico:.2f}"
        coluna["resultados"]["shops_premium_3x"]["text"] = f"Preço Shops Premium 3x: R${preco_shops_premium_3x:.2f}"
        coluna["resultados"]["shops_premium_12x"]["text"] = f"Preço Shops Premium 12x: R${preco_shops_premium_12x:.2f}"
        coluna["resultados"]["ml_classico"]["text"] = f"Preço ML Clássico: R${preco_ml_classico:.2f}"
        coluna["resultados"]["ml_premium_10x"]["text"] = f"Preço ML Premium 10x: R${preco_ml_premium_10x:.2f}"
        coluna["resultados"]["site"]["text"] = f"Preço Site: R${preco_site:.2f}"
        coluna["resultados"]["taxa_cliente"]["text"] = f"Valor Taxa Cliente ou Oficina: R${valor_taxa_cliente:.2f}"
    except ZeroDivisionError:
        messagebox.showerror("Erro de Cálculo", "Erro de divisão por zero.")
    except ValueError:
        limpar_resultados(coluna)


def processar(coluna, *_args):
    try:
        calcular_precos(coluna)
    except ValueError:
        limpar_resultados(coluna)


def criar_coluna(canvas, rotulo_x, entrada_x):
    coluna = {
        "vars": {
            "preco_custo": tk.StringVar(),
            "percentual_venda": tk.StringVar(),
            "frete": tk.StringVar(),
            "taxa_cliente_oficina": tk.StringVar(),
        },
        "resultados": {},
    }

    tk.Label(canvas, text="Preço Custo (R$):").place(x=rotulo_x, y=10)
    tk.Entry(canvas, textvariable=coluna["vars"]["preco_custo"]).place(x=entrada_x, y=10)

    tk.Label(canvas, text="Percentual de Venda (%):").place(x=rotulo_x, y=40)
    tk.Entry(canvas, textvariable=coluna["vars"]["percentual_venda"]).place(x=entrada_x, y=40)

    tk.Label(canvas, text="Frete (R$):").place(x=rotulo_x, y=70)
    tk.Entry(canvas, textvariable=coluna["vars"]["frete"]).place(x=entrada_x, y=70)

    tk.Label(canvas, text="Taxa Cliente ou Oficina (%):").place(x=rotulo_x, y=100)
    tk.Entry(canvas, textvariable=coluna["vars"]["taxa_cliente_oficina"]).place(x=entrada_x, y=100)

    coluna["resultados"]["shops_classico"] = tk.Label(canvas, text="", bg="yellow")
    coluna["resultados"]["shops_classico"].place(x=rotulo_x, y=130)

    coluna["resultados"]["shops_premium_3x"] = tk.Label(canvas, text="", bg="green")
    coluna["resultados"]["shops_premium_3x"].place(x=rotulo_x, y=160)

    coluna["resultados"]["shops_premium_12x"] = tk.Label(canvas, text="", bg="orange")
    coluna["resultados"]["shops_premium_12x"].place(x=rotulo_x, y=190)

    coluna["resultados"]["ml_classico"] = tk.Label(canvas, text="", bg="pink")
    coluna["resultados"]["ml_classico"].place(x=rotulo_x, y=220)

    coluna["resultados"]["ml_premium_10x"] = tk.Label(canvas, text="", bg="lightblue")
    coluna["resultados"]["ml_premium_10x"].place(x=rotulo_x, y=250)

    coluna["resultados"]["site"] = tk.Label(canvas, text="", bg="lightgray")
    coluna["resultados"]["site"].place(x=rotulo_x, y=280)

    coluna["resultados"]["taxa_cliente"] = tk.Label(canvas, text="", bg="lightcoral")
    coluna["resultados"]["taxa_cliente"].place(x=rotulo_x, y=310)

    for variavel in coluna["vars"].values():
        variavel.trace_add("write", lambda *_args, coluna=coluna: processar(coluna))

    return coluna


root = tk.Tk()
root.title("Calculadora de Preço e Lucro")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg=BACKGROUND_COLOR,
    highlightthickness=0,
)
canvas.pack(fill="both", expand=True)

COLUNA_ESQUERDA_X = 10
ENTRADA_ESQUERDA_X = 250
COLUNA_DIREITA_X = 420
ENTRADA_DIREITA_X = 660

coluna_esquerda = criar_coluna(canvas, COLUNA_ESQUERDA_X, ENTRADA_ESQUERDA_X)
coluna_direita = criar_coluna(canvas, COLUNA_DIREITA_X, ENTRADA_DIREITA_X)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Constantes para tipos de cimento
TIPOS_CIMENTO = {
    "Cimento Comum (CPI)": "Você escolheu o Cimento Portland Comum (CPI).",
    "Cimento Composto (CPII)": "Você escolheu o Cimento Portland Composto (CPII).",
    "Cimento de Alto Forno (CPIIII)": "Você escolheu o Cimento Portland de Alto Forno (CPIIII).",
    "Cimento Pozolânico (CPII-Z)": "Você escolheu o Cimento Portland Pozolânico (CPII-Z).",
    "Cimento de Alta Resistência Inicial (CPV-ARI)": "Você escolheu o Cimento Portland de Alta Resistência Inicial (CPV-ARI).",
}

# Classe que faz os cálculos do concreto
class Concreto:
    def __init__(self, resistencia_desejada, proporcao_cimento, proporcao_areia, proporcao_pedra):
        self.resistencia_desejada = resistencia_desejada
        self.proporcao_cimento = proporcao_cimento
        self.proporcao_areia = proporcao_areia
        self.proporcao_pedra = proporcao_pedra

    # Funções que realizam os cálculos dos ingredientes
    def calcular_ingredientes(self):
        quantidade_cimento = self.resistencia_desejada * self.proporcao_cimento
        quantidade_areia = self.resistencia_desejada * self.proporcao_areia
        quantidade_pedra = self.resistencia_desejada * self.proporcao_pedra
        return quantidade_cimento, quantidade_areia, quantidade_pedra

    @staticmethod
    def selecionar_cimento(tipo_cimento):
        cimentos = {
            'CP-I': {'fck': 25, 'descricao': 'Cimento Portland Comum'},
            'CP-II': {'fck': 32, 'descricao': 'Cimento Portland Composto'},
            'CP-III': {'fck': 40, 'descricao': 'Cimento Portland de Alto Forno'}
        }
        return cimentos.get(tipo_cimento, {'fck': 25, 'descricao': 'Cimento Padrão'})

# Realiza os cálculos dos materiais para o edifício
class CalculadoraMateriaisConstrucao:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def calculate_area(self):
        return self.length * self.width

    def calculate_volume(self):
        return self.length * self.width * self.height

    def calculate_materials(self):
        area = self.calculate_area()
        volume = self.calculate_volume()
        return {
            "Tinta": {"quantidade": area / 10, "unidade": "litros"},
            "Cimento": {"quantidade": volume * 0.02, "unidade": "kg"},
            "Azulejos": {"quantidade": area * 1.5, "unidade": "unidades"},
            "Areia": {"quantidade": volume * 0.5, "unidade": "m³"},
            "Tijolos": {"quantidade": volume * 12, "unidade": "unidades"}
        }

# Inicia a parte da interface coletando os dados do usuário
def calcular_tudo(entry_comprimento, entry_largura, entry_altura, entry_resistencia, entry_proporcao_cimento, entry_proporcao_areia, entry_proporcao_pedra, combo_tipo_cimento, text_resultados, frame_grafico):
    try:
        comprimento = float(entry_comprimento.get())
        largura = float(entry_largura.get())
        altura = float(entry_altura.get())
        calculator = CalculadoraMateriaisConstrucao(comprimento, largura, altura)
        materials_required = calculator.calculate_materials()

        resistencia_alvo = float(entry_resistencia.get())
        proporcao_cimento = float(entry_proporcao_cimento.get())
        proporcao_areia = float(entry_proporcao_areia.get())
        proporcao_pedra = float(entry_proporcao_pedra.get())
        tipo_cimento = combo_tipo_cimento.get()

        tipo_cimento_escolhido = TIPOS_CIMENTO.get(tipo_cimento, "Tipo de cimento inválido.")
        concreto = Concreto(resistencia_alvo, proporcao_cimento, proporcao_areia, proporcao_pedra)
        cimento, areia, pedra = concreto.calcular_ingredientes()

        result_text = "Materiais Necessários para o Edifício:\n"
        for material, details in materials_required.items():
            result_text += f"{material}: {details['quantidade']:.2f} {details['unidade']}\n"

        result_text += f"\n{tipo_cimento_escolhido}\n"
        result_text += f"Quantidade de cimento necessária: {cimento:.2f} kg\n"
        result_text += f"Quantidade de areia necessária: {areia:.2f} kg\n"
        result_text += f"Quantidade de pedra necessária: {pedra:.2f} kg\n"

        text_resultados.delete("1.0", tk.END)
        text_resultados.insert(tk.END, result_text)

        criar_grafico(materials_required, cimento, areia, pedra, frame_grafico)
        salvar_excel(materials_required, cimento, areia, pedra)
    except ValueError:
        messagebox.showerror("Erro de entrada", "Por favor, insira valores numéricos válidos.")

# Cria ou atualiza a planilha de documentos necessários
def salvar_excel(materials_required, cimento, areia, pedra):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Material", "Quantidade", "Unidade", "Descrição"])

    for material, details in materials_required.items():
        sheet.append([material, details["quantidade"], details["unidade"], ""])

    sheet.append(["Cimento", cimento, "kg", ""])
    sheet.append(["Areia", areia, "kg", ""])
    sheet.append(["Pedra", pedra, "kg", ""])

    workbook.save("materiais_calculados.xlsx")
    messagebox.showinfo("Sucesso", "Os resultados foram salvos no arquivo 'materiais_calculados.xlsx'")

# Cria um gráfico
def criar_grafico(materials_required, cimento, areia, pedra, frame_grafico):
    labels = list(materials_required.keys()) + ["Cimento", "Areia", "Pedra"]
    values = [details["quantidade"] for details in materials_required.values()] + [cimento, areia, pedra]

    fig = Figure(figsize=(10, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(labels, values, color='skyblue')
    ax.set_xlabel('Materiais')
    ax.set_ylabel('Quantidade')
    ax.set_title('Quantidade de Materiais Necessários')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, frame_grafico)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Cria e organiza a interface do usuário
def create_interface():
    root = tk.Tk()
    root.title("Calculadora de Materiais de Construção")

    frame_edificio = ttk.LabelFrame(root, text="Dados do Edifício")
    frame_edificio.grid(row=0, column=0, padx=10, pady=10)

    ttk.Label(frame_edificio, text="Comprimento (m):").grid(row=0, column=0, padx=5, pady=5)
    entry_comprimento = ttk.Entry(frame_edificio)
    entry_comprimento.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_edificio, text="Largura (m):").grid(row=1, column=0, padx=5, pady=5)
    entry_largura = ttk.Entry(frame_edificio)
    entry_largura.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_edificio, text="Altura (m):").grid(row= 2, column=0, padx=5, pady=5)
    entry_altura = ttk.Entry(frame_edificio)
    entry_altura.grid(row=2, column=1, padx=5, pady=5)

    frame_concreto = ttk.LabelFrame(root, text="Dados do Concreto")
    frame_concreto.grid(row=1, column=0, padx=10, pady=10)

    ttk.Label(frame_concreto, text="Resistência desejada (MPa):").grid(row=0, column=0, padx=5, pady=5)
    entry_resistencia = ttk.Entry(frame_concreto)
    entry_resistencia.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_concreto, text="Proporção de cimento:").grid(row=1, column=0, padx=5, pady=5)
    entry_proporcao_cimento = ttk.Entry(frame_concreto)
    entry_proporcao_cimento.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_concreto, text="Proporção de areia:").grid(row=2, column=0, padx=5, pady=5)
    entry_proporcao_areia = ttk.Entry(frame_concreto)
    entry_proporcao_areia.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_concreto, text="Proporção de pedra:").grid(row=3, column=0, padx=5, pady=5)
    entry_proporcao_pedra = ttk.Entry(frame_concreto)
    entry_proporcao_pedra.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_concreto, text="Tipo de cimento:").grid(row=4, column=0, padx=5, pady=5)
    combo_tipo_cimento = ttk.Combobox(frame_concreto, values=list(TIPOS_CIMENTO.keys()))
    combo_tipo_cimento.grid(row=4, column=1, padx=5, pady=5)

    frame_resultados = ttk.LabelFrame(root, text="Resultados")
    frame_resultados.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    text_resultados = tk.Text(frame_resultados, width=50, height=20)
    text_resultados.grid(row=0, column=0, padx=5, pady=5)

    frame_grafico = ttk.LabelFrame(root, text="Gráfico")
    frame_grafico.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    btn_calcular_tudo = ttk.Button(frame_concreto, text="Calcular Tudo", command=lambda: calcular_tudo(
        entry_comprimento, entry_largura, entry_altura, entry_resistencia, entry_proporcao_cimento,
        entry_proporcao_areia, entry_proporcao_pedra, combo_tipo_cimento, text_resultados, frame_grafico
    ))
    btn_calcular_tudo.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
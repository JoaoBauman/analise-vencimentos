import ipywidgets as widgets
from IPython.display import display, clear_output
from datetime import date, datetime

# --- Lógica de Negócio ---
def calcular_rebaixa(produto, vencimento, estoque, projecao):
    hoje = date.today()
    try:
        data_venc = datetime.strptime(vencimento, '%Y-%m-%d').date()
    except ValueError:
        return "Erro: Data de vencimento no formato inválido (use AAAA-MM-DD)."

    dias_para_vencer = (data_venc - hoje).days

    if dias_para_vencer < 0:
        return f"🚨 O produto {produto} já venceu (há {abs(dias_para_vencer)} dias)."

    # Projeção de venda por dia
    venda_diaria = projecao / 30
    dias_cobertura = estoque / venda_diaria if venda_diaria > 0 else 999

    resultado = f"📦 Produto: {produto}\n"
    resultado += f"🗓️ Dias para vencer: {dias_para_vencer} dias.\n"
    resultado += f"📊 Venda diária esperada: {venda_diaria:.2f} CX ou Kg.\n"
    resultado += f"⏱️ Estoque esgota em: {dias_cobertura:.1f} dias.\n\n"

    # Regra de negócio (exemplo: se vence em < 15 dias E cobertura > dias para vencer)
    if dias_para_vencer < 15 or dias_cobertura > dias_para_vencer:
        resultado += "⚠️ **RECOMENDAÇÃO: Ofertar com menor preço (Rebaixa de preço).**"
    else:
        resultado += "✅ **SITUAÇÃO NORMAL. Manter preço atual, mas na dúvida monitore.**"

    return resultado

# --- Interface Gráfica (ipywidgets) ---
# Inputs
txt_produto = widgets.Text(description="Produto:", placeholder="Nome/Abreviado")
date_vencimento = widgets.DatePicker(description="Vencimento:")
int_estoque = widgets.FloatText(description="Estoque (CX ou Kg):")
int_projecao = widgets.FloatText(description="Proj. venda (CX ou Kg):")

# Botões
btn_calcular = widgets.Button(description="Calcular", button_style='primary')
btn_limpar = widgets.Button(description="Limpar", button_style='warning')

# Saída
output = widgets.Output()

# Funções dos botões
def on_calcular_clicked(b):
    with output:
        clear_output()
        if not (txt_produto.value and date_vencimento.value and int_estoque.value and int_projecao.value):
            print("❌ Por favor, preencha todos os campos.")
            return

        res = calcular_rebaixa(
            txt_produto.value,
            date_vencimento.value.strftime('%Y-%m-%d'),
            int_estoque.value,
            int_projecao.value
        )
        print(res)

def on_limpar_clicked(b):
    txt_produto.value = ''
    date_vencimento.value = None
    int_estoque.value = 0
    int_projecao.value = 0
    with output:
        clear_output()

btn_calcular.on_click(on_calcular_clicked)
btn_limpar.on_click(on_limpar_clicked)

# Layout

form = widgets.VBox([
    widgets.HTML("<h2>Análise de Validade de Produto</h2>"),
    txt_produto, date_vencimento, int_estoque, int_projecao,
    widgets.HBox([btn_calcular, btn_limpar]),
    output
])

display(form)

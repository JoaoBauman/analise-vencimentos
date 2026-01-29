from flask import Flask, request, jsonify
from datetime import date, datetime
import os

app = Flask(__name__)

# --- Lógica de Negócio ---
def calcular_rebaixa(produto, vencimento, estoque, projecao):
    hoje = date.today()
    try:
        data_venc = datetime.strptime(vencimento, '%Y-%m-%d').date()
    except ValueError:
        return {"erro": "Data de vencimento no formato inválido (use AAAA-MM-DD)."}
    
    dias_para_vencer = (data_venc - hoje).days
    
    if dias_para_vencer < 0:
        return {
            "produto": produto,
            "status": "vencido",
            "mensagem": f"🚨 O produto {produto} já venceu (há {abs(dias_para_vencer)} dias)."
        }
    
    # Projeção de venda por dia
    venda_diaria = projecao / 30
    dias_cobertura = estoque / venda_diaria if venda_diaria > 0 else 999
    
    # Regra de negócio
    if dias_para_vencer < 15 or dias_cobertura > dias_para_vencer:
        recomendacao = "⚠️ **RECOMENDAÇÃO: Ofertar com menor preço (Rebaixa de preço).**"
    else:
        recomendacao = "✅ **SITUAÇÃO NORMAL. Manter preço atual, mas na dúvida monitore.**"
        
    return {
        "produto": produto,
        "dias_para_vencer": dias_para_vencer,
        "venda_diaria": round(venda_diaria, 2),
        "dias_cobertura": round(dias_cobertura, 1),
        "recomendacao": recomendacao
    }

# --- Webservice (Flask) ---
@app.route('/calcular', methods=['POST'])
def api_calcular():
    # Recebe os dados em formato JSON
    data = request.get_json()
    
    # Extrai os parâmetros
    produto = data.get('produto', 'Produto Desconhecido')
    vencimento = data.get('vencimento')
    estoque = float(data.get('estoque', 0))
    projecao = float(data.get('projecao', 0))
    
    if not vencimento:
        return jsonify({"erro": "Data de vencimento é obrigatória"}), 400
    
    # Processa
    resultado = calcular_rebaixa(produto, vencimento, estoque, projecao)
    
    # Retorna JSON
    return jsonify(resultado)

# Rota raiz para testar se o serviço está vivo
@app.route('/', methods=['GET'])
def home():
    return "Webservice de Rebaixa de Preço ativo. Use POST /calcular"

if __name__ == '__main__':
    # Render configura a porta automaticamente, ou usa 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

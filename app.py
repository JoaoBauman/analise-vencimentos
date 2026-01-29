from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def calculadora():
    # Obtém os parâmetros da URL: /?op=soma&n1=10&n2=5
    operacao = request.args.get('op')
    try:
        n1 = float(request.args.get('n1', 0))
        n2 = float(request.args.get('n2', 0))
    except ValueError:
        return "Erro: n1 e n2 devem ser números.", 400

    if operacao == 'soma':
        resultado = n1 + n2
    elif operacao == 'sub':
        resultado = n1 - n2
    elif operacao == 'mult':
        resultado = n1 * n2
    elif operacao == 'div':
        resultado = n1 / n2 if n2 != 0 else "Erro: Divisão por zero"
    else:
        return "Uso: /?op=[soma,sub,mult,div]&n1=X&n2=Y"

    return f"Resultado: {resultado}"

if __name__ == '__main__':
    app.run(host='74.220.48.0', port=24)

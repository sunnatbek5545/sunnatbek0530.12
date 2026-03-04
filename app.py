from flask import Flask, request, jsonify
from flask_cors import CORS
import sympy as sp
import re

app = Flask(__name__)
CORS(app)

# Noma'lumlar
x, y = sp.symbols('x y')

def clean_input(user_input):
    user_input = user_input.replace("^", "**")
    user_input = user_input.replace("√", "sqrt")
    # 2x -> 2*x formatiga o'tkazish
    user_input = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', user_input)
    # 50% -> (50/100) formatiga o'tkazish
    user_input = re.sub(r'(\d+(\.\d+)?)%', r'(\1/100)', user_input)
    return user_input

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    raw = data.get("equation", "").strip()
    if not raw: return jsonify({"error": "Bo'sh maydon!"}), 400

    try:
        raw = clean_input(raw)

        # Sistema bo'lsa (vergul bilan ajratilgan)
        if "," in raw:
            eqs = raw.split(",")
            equations = [sp.sympify(eq.split("=")[0]) - sp.sympify(eq.split("=")[1] if "=" in eq else "0") for eq in eqs]
            solution = sp.solve(equations, (x, y))
            # Natijani LaTeX formatiga o'tkazish
            latex_res = sp.latex(solution)
            return jsonify({"status": "success", "type": "system", "result": latex_res})

        # Oddiy tenglama
        else:
            if "=" in raw:
                left, right = raw.split("=")
                expr = sp.sympify(left) - sp.sympify(right)
            else:
                expr = sp.sympify(raw)

            vars_found = list(expr.free_symbols)
            var = vars_found[0] if vars_found else x
            solutions = sp.solve(expr, var)

            # Har bir yechimni LaTeX ko'rinishiga o'tkazish
            latex_solutions = [sp.latex(s) for s in solutions]
            return jsonify({"status": "success", "type": "equation", "solutions": latex_solutions})

    except Exception as e:
        return jsonify({"error": "Xato: Formatni tekshiring"}), 400

@app.route('/diff', methods=['POST'])
def derivative():
    data = request.get_json()
    try:
        expr = sp.sympify(clean_input(data.get("expression", "")))
        var = list(expr.free_symbols)[0] if expr.free_symbols else x
        res = sp.diff(expr, var)
        return jsonify({"status": "success", "result": sp.latex(res)})
    except: return jsonify({"error": "Hosila hisoblab bo'lmadi"}), 400

@app.route('/integrate', methods=['POST'])
def integral():
    data = request.get_json()
    try:
        expr = sp.sympify(clean_input(data.get("expression", "")))
        var = list(expr.free_symbols)[0] if expr.free_symbols else x
        res = sp.integrate(expr, var)
        return jsonify({"status": "success", "result": sp.latex(res)})
    except: return jsonify({"error": "Integral hisoblab bo'lmadi"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
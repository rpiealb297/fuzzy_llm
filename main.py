from typing import List, Set, Dict, Callable
from statistics import mean

valores_linguisticos = [
    "Perfecto", "Muy bien", "Bien", "Regular", "Malo", "Muy malo", "Incorrecto"
]

# Asignamos valores difusos entre 0 y 1 manualmente
fuzz_map = {
    "Perfecto": 0.95,
    "Muy bien": 0.9,
    "Bien": 0.75,
    "Regular": 0.5,
    "Malo": 0.25,
    "Muy malo": 0.1,
    "Incorrecto": 0.0
}


# ---------- dominance primitives ----------
def s(x: float, y: float) -> float:
    return 1.0 if x < y else 0.5 if x == y else 0.0

def r(x: float, y: float) -> float:
    return 0.5 * (y - x + 1.0)

def df_score(A: Set[float], B: Set[float],

    kernel: Callable[[float, float], float]) -> float:
    return mean(kernel(a, b) for a in A for b in B)

def dominance(A: Set[float], B: Set[float], method: str = "R") -> float:
    if method.upper() == "S":
        return df_score(A, B, s)
    elif method.upper() == "R":
        return df_score(A, B, r)
    else:
        raise ValueError("method␣must␣be␣’S’␣or␣’R’")

# ---------- pipeline ----------
def evaluate_text(
    expert_evals: List[Dict[str, Set[float]]],
    baselines: Dict[str, Set[float]],
    crit_weights: Dict[str, float]= None,
    expert_weights: List[float] = None,
    df_method: str = "R",
    pass_rule: Callable[[float], bool] = lambda W: W >= 0.5
    ):

    """Return accepted?, global score W, per-expert scores w_i."""
    m = len(baselines)
    if crit_weights is None:
        crit_weights = {c: 1.0 / m for c in baselines}
    if expert_weights is None:
        expert_weights = [1.0 / len(expert_evals)] * len(expert_evals)

    w_i: List[float] = []
    for E in expert_evals:
        d_vals = []
        for crit, B_k in baselines.items():
            A_ik = E[crit]
            d_vals.append(dominance(B_k, A_ik, df_method))
            # media ponderada sobre criterios
            w_i.append(sum(w * d for w, d in zip(
            (crit_weights[c] for c in baselines), d_vals)))
            # agregacin sobre expertos
        W = sum(w * wi for w, wi in zip(expert_weights, w_i))
    return pass_rule(W), W, w_i


# Función de fuzzificación
def fuzzimap(valor):
    return fuzz_map.get(valor, None)

def fuzzify_set(valores):
    items = set()
    for index in range(len(valores)):
        item = fuzzimap(valores[index])
        items.add(item)
    return items

# ---------- ejemplo rpido ----------
baselines = {
    "T_max": {0.8, 0.9},
    "RainProb": {0.7},
    "PhysCons": {0.6}
}


valores_expertos = [
    {"T_max": ["Perfecto"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]}
]

experts = []
for i in range(3):
    set_expertos = {}
    set_expertos["T_max"] = fuzzify_set(valores_expertos[i]["T_max"])
    set_expertos["RainProb"] = fuzzify_set(valores_expertos[i]["RainProb"])
    set_expertos["PhysCons"] = fuzzify_set(valores_expertos[i]["PhysCons"])
    experts.append(set_expertos)


'''
experts = [
    {"T_max": {0.75, 0.8}, "RainProb": {0.6, 0.65}, "PhysCons": {0.55, 0.6}},
    {"T_max": {0.7}, "RainProb": {0.6}, "PhysCons": {0.5, 0.55}},
    {"T_max": {0.82}, "RainProb": {0.75, 0.8}, "PhysCons": {0.6, 0.65}}
]
'''

'''
experts = [
    {"T_max": {0.9, 0.95}, "RainProb": {0.9, 0.95}, "PhysCons": {0.95, 0.9}},
    {"T_max": {0.7}, "RainProb": {0.6}, "PhysCons": {0.5, 0.55}},
    {"T_max": {0.82}, "RainProb": {0.75, 0.8}, "PhysCons": {0.6, 0.65}}
]
'''

print(experts)

accepted, W, w_i = evaluate_text(experts, baselines)
print("Global␣score:", W, "", "ACCEPTED" if accepted else "REJECTED")
print("Per-expert:", w_i)

import json
from sklearn.metrics import precision_score, recall_score, f1_score
from main import anonimizar  # Importa a sua função principal

# --- Carrega o Gabarito ---
def carregar_gold(path="gold_standard.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{path}' não encontrado.")
        return []

# --- Motor de Avaliação ---
def avaliar(modelo_func, gold_data):
    y_true = []
    y_pred = []

    print("--- INICIANDO BENCHMARK ---")
    
    for i, exemplo in enumerate(gold_data):
        texto = exemplo["texto"]
        # O gabarito diz quais tipos DEVEM ser encontrados (ex: {'CPF', 'EMAIL'})
        labels_true = set(exemplo["labels"])

        # O modelo roda e diz o que ACHOU
        achados, _ = modelo_func(texto)
        labels_pred = set([a["tipo"] for a in achados])

        # Compara o Gabarito com a Resposta do Modelo
        # Lógica simplificada: Se a classe existe no gabarito e no modelo = 1, senão 0
        todas_classes = labels_true.union(labels_pred)
        
        match = labels_true == labels_pred
        status = "✅" if match else "❌"
        print(f"Teste {i+1}: {status} | Esperado: {labels_true} | Encontrado: {labels_pred}")

        for classe in todas_classes:
            y_true.append(1 if classe in labels_true else 0)
            y_pred.append(1 if classe in labels_pred else 0)

    # Cálculo Matemático
    precisao = precision_score(y_true, y_pred, zero_division=0)
    sensibilidade = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    return precisao, sensibilidade, f1

if __name__ == "__main__":
    gold = carregar_gold()
    if gold:
        p, r, f1 = avaliar(anonimizar, gold)

        print("\n=== RELATÓRIO DE PERFORMANCE ===")
        print(f"PRECISÃO (Evitou Falsos Positivos?): {p:.2%}")
        print(f"RECALL   (Encontrou tudo?):          {r:.2%}")
        print(f"F1-SCORE (Média Harmônica):          {f1:.2%}")
        print("================================")

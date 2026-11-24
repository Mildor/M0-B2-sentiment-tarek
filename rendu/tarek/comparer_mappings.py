import json
from typing import Literal

Sentiment = Literal["négatif", "neutre", "positif"]

with open("scores_30_avis.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def best_star(scores: dict[str, float]) -> str:
    return max(scores, key=lambda k: scores[k])

def map_s(scores: dict[str, float]) -> str:
    groupes = {
        "négatif": scores.get("1 star", 0.0) + scores.get("2 stars", 0.0),
        "neutre": scores.get("3 stars", 0.0),
        "positif": scores.get("4 stars", 0.0) + scores.get("5 stars", 0.0)
    }
    return max(groupes, key=lambda k: groupes[k])

def map_a(star_label: str) -> Sentiment:
    star_label = star_label.strip().lower()

    match star_label:
        case '1 star' | '2 stars':
            return "négatif"
        case '3 stars':
            return "neutre"
        case '4 stars' | '5 stars':
            return "positif"
        case _:
            raise ValueError("star_label n'est pas dans le format attendu")

def map_b(star_label: str) -> Sentiment:
    star_label = star_label.strip().lower()

    match star_label:
        case '1 star':
            return "négatif"
        case '2 stars' | '3 stars':
            return "neutre"
        case '4 stars' | '5 stars':
            return "positif"
        case _:
            raise ValueError("star_label n'est pas dans le format attendu")

def map_c(star_label: str) -> Sentiment:
    star_label = star_label.strip().lower()

    match star_label:
        case '1 star' | '2 stars':
            return "négatif"
        case '4 stars' | '3 stars':
            return "neutre"
        case '5 stars':
            return "positif"
        case _:
            raise ValueError("star_label n'est pas dans le format attendu")


def map_exigeant(star_label: str) -> Sentiment:
    star_label = star_label.strip().lower()

    match star_label:
        case '1 star' | '2 stars' | '3 stars':
            return "négatif"
        case '4 stars':
            return "neutre"
        case '5 stars':
            return "positif"
        case _:
            raise ValueError("star_label n'est pas dans le format attendu")


LABELS: list[Sentiment] = ["négatif", "neutre", "positif"]

regles = {
    "Règle A (1-2 / 3 / 4-5)": lambda s: map_a(best_star(s)),
    "Règle B (1 / 2-3 / 4-5)": lambda s: map_b(best_star(s)),
    "Règle C (1-2 / 3-4 / 5)": lambda s: map_c(best_star(s)),
    "Règle S (somme des probas)": map_s,
    "Ma règle (1-2-3 / 4 / 5)": lambda s: map_exigeant(best_star(s)),
}

for nom_regle, fonction_regle in regles.items():
    matrice: dict[str, dict[str, int]] = {
        attendu: {predit: 0 for predit in LABELS} for attendu in LABELS
    }

    bien_classes = 0
    negatifs_manques = 0
    fausses_alertes = 0

    for row in data:
        attendu: str = row["attendu"]
        predit: str = fonction_regle(row["scores_5_stars"])

        matrice[attendu][predit] += 1

        if predit == attendu:
            bien_classes += 1

        if attendu == "négatif" and predit != "négatif":
            negatifs_manques += 1
        elif attendu != "négatif" and predit == "négatif":
            fausses_alertes += 1

    print("=" * 55)
    print(f"{nom_regle}")
    print("=" * 55)
    print(f"Bien classés     : {bien_classes} / {len(data)}")
    print(
        f"Négatifs manqués : {negatifs_manques} (client mécontent non rappelé)")
    print(
        f"Fausses alertes  : {fausses_alertes} (responsable dérangé pour rien)\n")

    print(f"{'Attendu':<8} \\ {'Prédit':<7} | {'négatif':>8} | {'neutre':>8} | {'positif':>8}") 
    print("-" * 51)
    for attendu in LABELS:
        row_vals = matrice[attendu]
        print(
            f"{attendu:<18} | {row_vals['négatif']:>8} | {row_vals['neutre']:>8} | {row_vals['positif']:>8}"
        )
    print("\n")

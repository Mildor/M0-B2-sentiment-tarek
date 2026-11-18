"""Logique d'inférence pour la classification de sentiment.

Le modèle CamemBERT chargé sort des labels 5 étoiles
(`'1 star'`, `'2 stars'`, ..., `'5 stars'`). Le métier (Aubergine Hôtels)
veut 3 classes (`négatif`, `neutre`, `positif`).

→ Ton travail dans ce fichier :
   1. Implémenter `predict_sentiment()` (récupère les scores 5★ + applique ta règle).
   2. Implémenter `map_stars_to_sentiment()` (mapping 5★ → 3 classes).
   3. Écrire ta règle dans le commentaire `# DECISION:` ci-dessous AVANT de coder.

Le pipeline transformers est chargé une seule fois au démarrage, dans
`main.py` (lifespan), et stocké dans `state["pipeline"]`. Tu le récupères
en argument.
"""
from __future__ import annotations

# DECISION: (à écrire avant de coder, en français)
#   Règle retenue : B exigeant 1-2-3 -> négatif 4 -> neutre 5 -> positif
#   Capturer les avis moyen mitigé (3 stars) dans la fil prioritaire négatif permettra de régler et paufiner des problemes qui sont en général pas pris en compte (avis moyen)
#   en mettant les avis neutre en 4 (des séjours généralement bon) l'équipe ne perdera pas de temps a traiter de bon séjours.
#   De plus les études du secteur hôtelier (Cornell University / TripAdvisor),  démontrent qu'en dessous de 4/5 la moyenne chute en la tirant vers le bas

import time
from typing import Any

from app.schemas import Sentiment, SentimentOut


def map_stars_to_sentiment(star_label: str) -> Sentiment:
    """Mappe un label 5 étoiles ('1 star', ..., '5 stars') en 3 classes métier.

    Args:
        star_label: label produit par le modèle (ex: '4 stars').

    Returns:
        Sentiment 3 classes.

    Raises:
        ValueError: si `star_label` n'est pas dans le format attendu.
    """
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


def predict_sentiment(pipeline: Any, text: str, model_name: str) -> SentimentOut:
    """Inférence de sentiment sur un texte FR.

    Args:
        pipeline: pipeline `transformers.pipeline("text-classification", ...)`
            chargé au démarrage de l'API.
        text: texte FR de la review.
        model_name: identifiant HF du modèle (passé pour traçabilité).

    Returns:
        SentimentOut avec sentiment 3 classes, scores 5★ bruts, et latence ms.
    """
    starter = time.perf_counter()
    raw = pipeline(text)
    scores_5_stars = {}
    for item in raw[0]:
        scores_5_stars[item["label"]] = item["score"]

    best_star = max(scores_5_stars, key=lambda k: scores_5_stars[k])
    sentiment = map_stars_to_sentiment(best_star)

    time_spent_ms = (time.perf_counter() - starter) * 1000
    return SentimentOut(
        sentiment=sentiment,
        scores_5_stars=scores_5_stars,
        model_name=model_name,
        latence_ms=time_spent_ms
    )

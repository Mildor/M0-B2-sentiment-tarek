from __future__ import annotations

from fastapi.testclient import TestClient
import pytest
from app.main import app


def test_predict_positif() -> None:
    """POST /predict retourne 200 et un sentiment valide."""
    with TestClient(app) as client:
        payload = {
            "texte": "Séjour parfait, hôtel magnifique et personnel aux petits soins !"
            # "texte": "Accueil glacial à la réception, chambre froide et bruyante, nous ne reviendrons pas."
        }
        response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["sentiment"] == "positif"
    

@pytest.mark.parametrize("texte_invalide", ["", "   ", "a" * 2001])
def test_predict_texte_null_toolong(texte_invalide: str) -> None:
    """POST /predict retourne 422 si le texte est vide ou trop long."""
    with TestClient(app) as client:
        response = client.post("/predict", json={"texte": texte_invalide})
    assert response.status_code == 422
    
    
@pytest.mark.parametrize(
    "texte, attendu",
    [
        ("Personnel charmant, chambre impeccable, petit-déjeuner copieux. On reviendra avec plaisir.", "positif"),
        ("Bonne situation centrale, parking pratique. Chambre un peu petite mais bien insonorisée.", "neutre"),
        ("Annulez votre réservation tant qu'il est temps. Service inexistant, chambre douteuse, prix abusif.", "négatif"),
    ],
)
def test_predict_all_sentiment(texte: str, attendu: str) -> None:
    """POST /predict retourn 200"""
    with TestClient(app) as client:
        payload = {
            "texte": texte
        }
        response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["sentiment"] == attendu
# M0-B2 — Bonus (pour ceux qui ont fini)

> Seulement une fois les tâches 1 à 6 et les livrables A à D **terminés et mergés dans `main`**.
> Un bonus ne rattrape pas un livrable manquant.
> Chaque bonus se fait seul. Choisis-en un ou plusieurs, dans l'ordre que tu veux.
> **Ordre conseillé : H → G → F → E** (du plus proche du cœur du brief au plus technique).

| # | Bonus | Durée | Ce qu'il travaille |
|---|---|---|---|
| H | Mesurer l'effet d'un autre découpage 5★ → 3 classes | ≈ 1 h 15 | Le mapping comme choix mesurable, et les limites d'une petite évaluation |
| G | « Pourquoi pas un LLM généraliste ? » | ≈ 1 h | Arbitrer avec des faits, pas par effet de mode |
| F | Endpoint `/predict/batch` | ≈ 1 h | Concevoir un contrat d'API, mesurer un gain |
| E | Healthcheck dimensionné sur la réalité | ≈ 45 min | Régler un healthcheck sur des mesures, pas au hasard |

**Où rendre** : un fichier `rendu/<prenom>/BONUS.md`, une section par bonus fait. Le code (F, E) va sur ta branche, comme le reste.
⚠️ F et E modifient des fichiers communs (`app/main.py`, `docker-compose.yml`) : préviens ton binôme avant, pour ne pas vous marcher dessus au merge.

---

## H — Mesurer l'effet d'un autre découpage 5★ → 3 classes

### Pourquoi

Tu as choisi un mapping en tâche 3 et tu l'as justifié avec des arguments métier (livrable D). Ici, tu le confrontes aux chiffres : que se passe-t-il sur les 30 avis si on découpe autrement ? Et que valent vraiment ces chiffres ?

### Ce que tu fais

**1. Récupérer les scores 5★ des 30 avis, une seule fois (≈ 15 min).**
Ton API renvoie déjà `scores_5_stars` : pas besoin de rappeler le modèle pour chaque découpage. Le script ci-dessous n'utilise que la bibliothèque standard Python (pas d'environnement virtuel à créer). Lance-le **sur ta machine**, depuis la racine du repo, stack démarrée :

```python
# rendu/<prenom>/recuperer_scores.py — Python 3.11+, bibliothèque standard seule
import csv
import json
import urllib.request
from pathlib import Path

API = "http://localhost:8000/predict"
SORTIE = Path(__file__).parent / "scores_30_avis.json"

resultats = []
with open("data/sample_reviews.csv", encoding="utf-8") as f:
    for ligne in csv.DictReader(f):
        requete = urllib.request.Request(
            API,
            data=json.dumps({"texte": ligne["texte"]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(requete, timeout=30) as reponse:
            corps = json.load(reponse)
        resultats.append({
            "id": int(ligne["id"]),
            "attendu": ligne["sentiment_attendu"],
            "note_client": int(ligne["note_client"]),
            "scores_5_stars": corps["scores_5_stars"],
        })

SORTIE.write_text(json.dumps(resultats, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(resultats)} avis enregistrés dans {SORTIE}")
```

**2. Écrire `comparer_mappings.py` (≈ 30 min).** À toi de l'écrire. Il lit `scores_30_avis.json` et applique **au moins 4 règles** :

| Règle | Étoile retenue | Négatif | Neutre | Positif |
|---|---|---|---|---|
| A | la plus probable | 1-2 | 3 | 4-5 |
| B | la plus probable | 1 | 2-3 | 4-5 |
| C | la plus probable | 1-2 | 3-4 | 5 |
| S | aucune : on **somme les probabilités** par groupe (1-2 / 3 / 4-5), le plus gros total l'emporte | | | |

Si ta règle de la tâche 3 n'est dans aucune de ces lignes, ajoute-la.

Pour chaque règle, le script affiche :
- le nombre d'avis bien classés sur 30 ;
- la **matrice de confusion** 3 × 3 (attendu en lignes, prédit en colonnes) ;
- deux erreurs qui n'ont pas le même coût pour Aubergine Hôtels :
  - **négatifs manqués** : avis attendu `négatif`, prédit autre chose (un client mécontent que personne ne rappelle) ;
  - **fausses alertes** : avis attendu `positif` ou `neutre`, prédit `négatif` (un responsable d'hôtel dérangé pour rien).

Indice : un `dict` de compteurs suffit pour la matrice. Pas besoin de pandas ni de scikit-learn.

**3. Analyser (≈ 30 min), dans `rendu/<prenom>/BONUS.md` section H.** Réponds à ces 4 questions, chiffres à l'appui :

1. Quelle règle classe le plus d'avis correctement ? Quelle règle manque le moins de négatifs ? Est-ce la même ?
2. Combien d'avis séparent la meilleure règle de la tienne ? Sur 30 avis, **un avis = 3,3 points**. Un écart de 1 ou 2 avis te paraît-il suffisant pour changer de règle ? Pourquoi ?
3. Ouvre `data/sample_reviews.csv` et compare les colonnes `note_client` et `sentiment_attendu`. Comment le sentiment attendu semble-t-il avoir été fabriqué ? Qu'est-ce que ça implique pour la comparaison que tu viens de faire ?
4. Si tu choisis la règle qui gagne sur ces 30 avis, puis que tu annonces son score au client, ce score est-il fiable ? Que te faudrait-il pour l'affirmer ?

Termine par une phrase de décision : tu gardes ta règle, ou tu changes, et pourquoi.

### Terminé quand

- [ ] `recuperer_scores.py`, `comparer_mappings.py` et `scores_30_avis.json` sont dans `rendu/<prenom>/`
- [ ] La sortie du script (copiée telle quelle) est dans `BONUS.md`, pour les 4 règles au moins
- [ ] Les 4 questions ont une réponse chiffrée
- [ ] Une décision finale est écrite, et elle tient compte des questions 2 à 4

### Si ça coince

| Symptôme | Cause probable |
|---|---|
| `ConnectionRefusedError` | Stack arrêtée, ou script lancé depuis le conteneur au lieu de ta machine |
| `HTTPError 501` | `/predict` n'est pas branché (tâche 3), ou conteneur pas reconstruit (`docker compose up --build`) |
| `FileNotFoundError: data/sample_reviews.csv` | Script lancé hors de la racine du repo |
| Les 4 règles donnent exactement les mêmes chiffres | Le modèle ne prédit presque jamais 2★ ni 4★ : regarde la distribution des étoiles retenues, c'est déjà un résultat à écrire |

---

## G — « Pourquoi pas un LLM généraliste ? »

### Pourquoi

Le client demandera tôt ou tard : « Pourquoi pas ChatGPT ? ». La mauvaise réponse est un avis général (« les LLM, c'est cher »). La bonne s'appuie sur ce que **tu** as observé sur **ce** cas.

### Ce que tu fais

Une page maximum dans `rendu/<prenom>/BONUS.md` section G, organisée en 5 critères. Pour chacun, **un fait chiffré ou observé** côté CamemBERT, puis ce que tu sais (ou supposes, en le disant) côté LLM :

| Critère | Côté CamemBERT : d'où tirer le fait |
|---|---|
| Latence | `latence_ms` de tes réponses `/predict` (ou tes logs `logs/api.log`) |
| Coût | Il tourne sur ton portable, sans GPU. Combien d'avis Aubergine reçoit-il par jour, à ton avis ? Fais une estimation de coût pour 10 000 avis par mois avec un LLM payant, en citant la page de prix utilisée et sa date |
| Format de sortie | Toujours une des 3 classes, garanti par le schéma Pydantic. Un LLM répond en texte libre : qu'est-ce qu'il faudrait ajouter pour obtenir le même contrat ? |
| Reproductibilité | Même texte, même réponse, à chaque appel ? Teste 3 fois le même avis |
| Données | Les vrais avis clients peuvent contenir des noms, des numéros de chambre. Où partent-ils avec un LLM en API externe ? |

**Option (facultative, +30 min)** : soumets à un LLM (Ollama en local, ou un chat en ligne : ces avis sont fictifs, ça ne pose pas de problème) **tes 3 avis mal classés du livrable B**. Note s'il fait mieux, en combien de temps, et si sa réponse est directement exploitable par une API. Ne conclus pas sur 3 avis : dis ce que ça suggère, pas ce que ça prouve.

Termine par une recommandation pour Aubergine Hôtels, en 3 lignes. « Un LLM n'est jamais justifié » et « un LLM est toujours mieux » sont deux mauvaises réponses : dans quel cas, précisément, changerais-tu d'avis ?

### Terminé quand

- [ ] Les 5 critères ont chacun au moins un fait issu de tes mesures ou de ta lecture (source citée)
- [ ] Les suppositions sont signalées comme telles
- [ ] La recommandation nomme au moins une condition qui la ferait changer

---

## F — Endpoint `/predict/batch`

### Pourquoi

Aubergine Hôtels veut requalifier chaque nuit les avis de la veille. 500 appels HTTP l'un après l'autre, ou un seul appel avec un lot ? Tu conçois le contrat de l'endpoint, puis tu **mesures** si le lot fait vraiment gagner du temps.

### Ce que tu fais

**1. Le contrat (≈ 15 min).** Dans `app/schemas.py`, crée :
- `BatchIn` : un champ `textes`, liste de 1 à 32 textes, chacun avec les mêmes règles que `ReviewIn` (non vide, pas uniquement des espaces, au plus `MAX_TEXT_LENGTH`) ;
- `BatchOut` : la liste des `SentimentOut`, **dans le même ordre que l'entrée**, plus la latence totale.

Écris dans `BONUS.md` pourquoi tu limites le lot (à 32 ou à une autre valeur que tu justifies). Pense à la mémoire du conteneur et au temps de réponse maximal acceptable.

**2. Version 1 : une boucle (≈ 15 min).** `POST /predict/batch` appelle `predict_sentiment()` pour chaque texte. Réutilise le code de `/predict` : pas de copier-coller de la logique de mapping.

**3. Version 2 : le pipeline en lot (≈ 15 min).** Le pipeline transformers accepte une **liste** de textes en une fois (`pipeline(liste_de_textes)`) et renvoie une liste de résultats. Adapte ton code pour l'utiliser. Attention à la forme du résultat : elle n'est pas la même qu'avec un seul texte.

**4. Mesurer (≈ 15 min).** Avec les 30 avis du CSV (en 1 lot de 30) :
- durée de 30 appels `/predict` successifs ;
- durée de `/predict/batch` version 1 ;
- durée de `/predict/batch` version 2.

Fais chaque mesure 3 fois et garde la médiane. Note-les dans `BONUS.md`, sur la même machine, et explique l'écart en 3 lignes.

**5. Tester.** Dans `tests/`, au moins 3 tests : un lot de 3 textes → 200, 3 résultats dans le bon ordre ; liste vide → 422 ; 33 textes → 422.

### Terminé quand

- [ ] `/predict/batch` apparaît dans Swagger (`/docs`) avec ses schémas
- [ ] `docker compose exec api-nlp pytest -v` passe, y compris tes 3 nouveaux tests
- [ ] Les 3 mesures (médianes) et l'explication sont dans `BONUS.md`
- [ ] `/predict` fonctionne toujours exactement comme avant

---

## E — Healthcheck dimensionné sur la réalité

### Pourquoi

Le healthcheck du `docker-compose.yml` a été réglé « à vue » (`start_period: 40s`, `retries: 3`). Est-ce adapté au vrai temps de chargement du modèle ? Et l'interface Streamlit démarre sans attendre que l'API soit prête (`condition: service_started`) : que voit un utilisateur pendant ce temps ?

### Ce que tu fais

**1. Mesurer (≈ 15 min).** Chronomètre le temps entre `docker compose up` et le passage à `healthy` dans `docker compose ps` :
- **à froid** : supprime le cache du modèle (`models/`, vérifie que c'est bien le cache, pas autre chose) et relance ;
- **à chaud** : relance avec le cache déjà rempli.

Note les deux durées dans `BONUS.md`.

**2. Observer le problème (≈ 10 min).** Pendant un démarrage, ouvre l'UI Streamlit avant que l'API soit `healthy` et envoie un avis. Note ce que voit l'utilisateur.

**3. Régler (≈ 15 min).** Dans `docker-compose.yml` :
- ajuste `start_period`, `interval` et `retries` à partir de tes mesures, en commentant chaque valeur (« à froid j'ai mesuré X s, donc… ») ;
- fais attendre l'UI : `condition: service_healthy`.

Explique dans `BONUS.md` la différence entre `start_period` et `retries` : pendant `start_period`, que se passe-t-il quand un test échoue ?

**4. Question à trancher (≈ 5 min).** Un `start_period` de 10 minutes « pour être tranquille » : quel est le problème ?

### Terminé quand

- [ ] Les durées à froid et à chaud sont mesurées et notées
- [ ] Chaque valeur du healthcheck a un commentaire qui la relie à une mesure
- [ ] L'UI attend que l'API soit `healthy`, et `docker compose ps` le montre
- [ ] La question du `start_period` de 10 minutes a une réponse

# Bonus — M0-B2 Aubergine Hôtels

## H — Mesurer l'effet d'un autre découpage 5★ → 3 classes

### Sortie de `comparer_mappings.py`

```text
=======================================================
Règle A (1-2 / 3 / 4-5)
=======================================================
Bien classés     : 24 / 30
Négatifs manqués : 3 (client mécontent non rappelé)
Fausses alertes  : 1 (responsable dérangé pour rien)

Attendu  \ Prédit  |  négatif |   neutre |  positif
---------------------------------------------------
négatif            |        8 |        2 |        1
neutre             |        1 |        6 |        1
positif            |        0 |        1 |       10


=======================================================
Règle B (1 / 2-3 / 4-5)
=======================================================
Bien classés     : 21 / 30
Négatifs manqués : 7 (client mécontent non rappelé)
Fausses alertes  : 0 (responsable dérangé pour rien)

Attendu  \ Prédit  |  négatif |   neutre |  positif
---------------------------------------------------
négatif            |        4 |        6 |        1
neutre             |        0 |        7 |        1
positif            |        0 |        1 |       10


=======================================================
Règle C (1-2 / 3-4 / 5)
=======================================================
Bien classés     : 21 / 30
Négatifs manqués : 3 (client mécontent non rappelé)
Fausses alertes  : 1 (responsable dérangé pour rien)

Attendu  \ Prédit  |  négatif |   neutre |  positif
---------------------------------------------------
négatif            |        8 |        3 |        0
neutre             |        1 |        7 |        0
positif            |        0 |        5 |        6


=======================================================
Règle S (somme des probas)
=======================================================
Bien classés     : 25 / 30
Négatifs manqués : 1 (client mécontent non rappelé)
Fausses alertes  : 2 (responsable dérangé pour rien)

Attendu  \ Prédit  |  négatif |   neutre |  positif
---------------------------------------------------
négatif            |       10 |        0 |        1
neutre             |        2 |        5 |        1
positif            |        0 |        1 |       10


=======================================================
Ma règle (1-2-3 / 4 / 5)
=======================================================
Bien classés     : 17 / 30
Négatifs manqués : 1 (client mécontent non rappelé)
Fausses alertes  : 8 (responsable dérangé pour rien)

Attendu  \ Prédit  |  négatif |   neutre |  positif
---------------------------------------------------
négatif            |       10 |        1 |        0
neutre             |        7 |        1 |        0
positif            |        1 |        4 |        6
```

---

### Analyse

#### 1. Quelle règle classe le plus d'avis correctement ? Quelle règle manque le moins de négatifs ? Est-ce la même ?

- **Règle qui classe le plus d'avis correctement :** la **Règle S (somme des probas)** arrive en tête avec **25 / 30** avis bien classés (**83,3 %**), juste devant la **Règle A** (**24 / 30**, soit 80,0 %), suivies des **Règles B et C** (**21 / 30**, soit 70,0 %), puis de **Ma règle (`1-2-3 / 4 / 5`)** (**17 / 30**, soit 56,7 %).
- **Règle qui manque le moins de négatifs :** la **Règle S** et **Ma règle (`1-2-3 / 4 / 5`)** sont ex aequo avec **1 seul négatif manqué sur 11** (contre 3 pour les Règles A et C, et 7 pour la Règle B). En revanche, pour ce même niveau de rappel sur les négatifs, la Règle S ne génère que **2 fausses alertes**, contre **8 fausses alertes** pour ma règle.
- **Est-ce la même ?** **Oui** : la **Règle S** est à la fois celle qui obtient le meilleur score global (25 / 30) et (ex aequo avec ma règle) celle qui rate le moins d'avis négatifs (1 / 11).

#### 2. Combien d'avis séparent la meilleure règle de la tienne ? Sur 30 avis, un avis = 3,3 points. Un écart de 1 ou 2 avis te paraît-il suffisant pour changer de règle ? Pourquoi ?

- La meilleure règle (**Règle S**, 25 / 30) et la mienne (**`1-2-3 / 4 / 5`**, 17 / 30) sont séparées par **8 avis**, soit **26,7 points** d'écart (83,3 % contre 56,7 %).
- **Un écart de 1 ou 2 avis (3,3 à 6,7 points) ne serait absolument pas suffisant pour changer de règle**, pour deux raisons :
  1. **Taille d'échantillon trop faible ($n = 30$) :** sur 30 avis, la variance d'échantillonnage est très forte (marge d'erreur de l'ordre de $\pm 15$ à $\pm 18$ points à 95 % de confiance). Un écart de 1 ou 2 avis peut s'inverser sur un autre échantillon de 30 avis.
  2. **Coût asymétrique des erreurs :** le taux global de bonnes réponses ne distingue pas un négatif manqué (coût élevé : client mécontent non rappelé) d'une fausse alerte (coût plus faible). Une règle peut être légèrement en dessous en accuracy tout en protégeant mieux le métier.
- Ici, l'écart est nettement plus grand (8 avis), mais il faut d'abord vérifier d'où vient cet écart (question 3) avant d'en tirer une conclusion définitive.

#### 3. Ouvre `data/sample_reviews.csv` et compare les colonnes `note_client` et `sentiment_attendu`. Comment le sentiment attendu semble-t-il avoir été fabriqué ? Qu'est-ce que ça implique pour la comparaison que tu viens de faire ?

- En comparant `note_client` et `sentiment_attendu` sur les 30 lignes de `data/sample_reviews.csv`, la correspondance est **strictement mécanique** :
  - `note_client` = `1` (9 avis) ou `2` (2 avis) $\rightarrow$ `négatif` (11 avis) ;
  - `note_client` = `3` (8 avis) $\rightarrow$ `neutre` (8 avis) ;
  - `note_client` = `4` (4 avis) ou `5` (7 avis) $\rightarrow$ `positif` (11 avis).
- Le `sentiment_attendu` a donc été **fabriqué en appliquant exactement la Règle A (`1-2 / 3 / 4-5`)** à la note client.
- **Ce que ça implique pour la comparaison :**
  - Le jeu d'évaluation **favorise par construction les règles alignées sur `1-2 / 3 / 4-5`** (Règle A et Règle S).
  - À l'inverse, **Ma règle (`1-2-3 / 4 / 5`)** (ainsi que B et C) est **pénalisée artificiellement** : même lorsque le modèle prédit la bonne note (`3 stars` ou `4 stars`), le mapping la classe en `négatif` (pour `3`) ou `neutre` (pour `4`), ce qui est compté comme erreur face à `sentiment_attendu`. Sur les 13 erreurs de ma règle, **11 proviennent directement de ce décalage de définition** (7 avis `neutre` classés `négatif` et 4 avis `positif` classés `neutre`).
  - Cette comparaison mesure donc davantage la **proximité avec la convention d'étiquetage du CSV** que la pertinence métier réelle des règles.

#### 4. Si tu choisis la règle qui gagne sur ces 30 avis, puis que tu annonces son score au client, ce score est-il fiable ? Que te faudrait-il pour l'affirmer ?

- **Non, ce score (25 / 30 = 83,3 %) n'est pas fiable pour être annoncé au client** comme performance attendue en production :
  1. **Échantillon trop petit et non représentatif ($n = 30$) :** l'incertitude statistique est trop large sur 30 avis, et ces 30 exemples ne couvrent pas toute la variété des vrais avis clients (avis très longs, fautes d'orthographe, argot, ironie complexe).
  2. **Sélection et évaluation sur le même jeu :** choisir la règle gagnante sur ces 30 avis puis annoncer son score sur ces mêmes 30 avis introduit un biais optimiste.
  3. **Vérité terrain conventionnelle :** `sentiment_attendu` reflète une règle `1-2 / 3 / 4-5` issue des notes, pas une validation humaine des priorités de rappel d'Aubergine Hôtels.
- **Ce qu'il faudrait pour pouvoir l'affirmer :**
  1. Un **jeu de test indépendant et beaucoup plus large** (au moins 300 à 500 avis réels représentatifs des hôtels du groupe), distinct de tout jeu ayant servi à choisir la règle.
  2. Une **vérité terrain annotée selon le besoin métier réel** (quels avis doivent déclencher un rappel client vs rester neutres/positifs), idéalement avec double annotation.
  3. Des **métriques orientées métier** (rappel sur les négatifs, taux de fausses alertes, matrice de confusion) accompagnées d'un intervalle de confiance.

---

### Décision finale

Je change de règle pour adopter la Règle S : à sécurité égale sur les clients mécontents, elle divise par quatre les fausses alertes tout en exploitant l'ensemble de la distribution de probabilités du modèle, ce choix devra toutefois être confirmé sur un jeu de validation plus large avant d'annoncer un score de performance au client.

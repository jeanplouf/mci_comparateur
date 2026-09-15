# mci_comparateur

Réimplémentation en Python du **Material Circularity Indicator** (MCI) de la
Fondation Ellen MacArthur : un indicateur, entre 0 et 1, qui mesure à quel point
les flux de matière d'un produit sont circulaires plutôt que linéaires.

Projet d'apprentissage : l'objectif est le code (POO, fonctions pures, tests,
validation, persistance, CLI), le MCI servant de support métier.

## Ce que fait le programme

- calcule le MCI d'un produit à partir de ses caractéristiques matière et usage
- compare plusieurs produits entre eux
- sauvegarde et recharge un catalogue de produits en JSON
- interface en ligne de commande pour saisir, calculer, sauvegarder

## Le modèle

MCI = 1 − LFI × F(X)

- **LFI** (*Linear Flow Index*) — part des flux de matière qui suivent un chemin
  linéaire : matière vierge en entrée, enfouissement en sortie, pertes de
  recyclage incluses.
- **F(X) = 0.9 / X** — facteur d'utilité, avec
  `X = (L/L_av) × (U/U_av)`. Plus un produit dure et sert, moins sa linéarité
  pèse.

Le résultat est borné à 0.

### Périmètre

Le MCI ne mesure **que les flux de matière**. Il ignore volontairement le
transport, l'énergie, les émissions (domaine de l'Analyse de Cycle de Vie) et
les coûts. C'est un choix méthodologique du modèle, pas une limite de cette
implémentation.

### Note sur les moyennes sectorielles

`L_av` et `U_av` ne font l'objet d'aucune table de référence officielle : la
méthode laisse à l'utilisateur le soin de les établir. Les valeurs présentes
dans `SECTEURS` sont **indicatives** et servent à faire tourner le programme.
Elles sont à remplacer par des données sectorielles documentées pour tout usage
réel — et un score MCI n'est interprétable qu'accompagné des hypothèses qui
l'ont produit.

## Installation

```bash
git clone git@github.com:jeanplouf/mci_comparateur.git
cd mci_comparateur
conda create -n mci python=3.11
conda activate mci
pip install -r requirements.txt
```

## Utilisation

```bash
python mci.py
```

Le menu propose d'ajouter un produit, d'afficher les scores, de sauvegarder et
de recharger un catalogue.

## Tests

```bash
pytest
```

## Structure

| Fichier | Rôle |
|---|---|
| `mci.py` | formules, classe `Produit`, persistance, CLI |
| `test_mci.py` | suite de tests |
| `produits.json` | catalogue sauvegardé |

## Source

Ellen MacArthur Foundation — *Circularity Indicators: An Approach to Measuring
Circularity* (méthodologie alignée ISO 59020).
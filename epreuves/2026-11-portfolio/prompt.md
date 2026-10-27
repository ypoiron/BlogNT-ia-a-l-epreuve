# Prompt (identique pour tous les outils)

```
Crée la page d'accueil de mon portfolio personnel. Je suis Yohann Poiron, fondateur et rédacteur en chef de BlogNT, média tech indépendant depuis 2011. Mon CV est joint. Tu as l'autorisation de rechercher des informations publiques à mon sujet.

Démarche obligatoire :
1. Recherche : lis mon CV, puis cherche des informations publiques sur moi. Vérifie chaque fait avec au moins une source.
2. Questions : pose-moi entre 3 et 5 questions de clarification avant de concevoir quoi que ce soit.
3. Direction artistique : propose une direction graphique adaptée à ma personnalité et explique-la en 3 lignes.
4. Développement : construis une page d'accueil complète, responsive, avec modes clair et sombre.
5. Vérification : contrôle les liens, l'accessibilité (contrastes, textes alternatifs, navigation clavier) et l'affichage mobile.

Règles :
- N'invente jamais de références, de chiffres, de clients ni de témoignages.
- N'expose aucune donnée privée (adresse, téléphone personnel) sans mon accord.
- Les textes doivent raconter mon parcours et donner envie d'en savoir plus, pas aligner des informations.
```

Écart constaté dans les journaux : Claude Code a reçu « Mon CV (Profile (1).pdf) est joint dans le dossier. » à la place de « Mon CV est joint. » (le reste est identique). Codex a reçu le CV en pièce jointe de l'application. Le premier message de Lovable n'est pas dans son journal : non vérifié.

## Réponses données aux questions des outils

Les outils n'ont pas posé les mêmes questions : les réponses ont été données au fil de l'eau, d'après les journaux.

| Outil | Thème de la question | Réponse donnée |
| --- | --- | --- |
| Claude Code | Public prioritaire | Santé numérique (recommandé) |
| Claude Code | Date de création de BlogNT, chiffres du site | 2011, sans chiffres |
| Claude Code | Coordonnées publiées | LinkedIn, e-mail |
| Claude Code | Ton des textes, version anglaise | FR sobre et narratif |
| Codex | Rôle de BlogNT sur la page | Un équilibre entre les deux |
| Codex | Public visé | Santé numérique |
| Codex | Liens à afficher | LinkedIn et e-mail |
| Codex | Photo, logo, identité visuelle | Construire la page autour de la typographie et de formes graphiques |
| Lovable | Facette dominante de la page | Les deux à égalité |
| Lovable | Date de création de BlogNT | 2011 |
| Lovable | Moyens de contact publics | LinkedIn, e-mail |
| Lovable | Photo | Non, pas de photo |

## Questions posées par chaque outil

### Claude Code
Quatre questions posées en une fois, dont deux doubles (6 sous-questions) :
1. Quel public doit viser la page d'accueil en priorité ?
2. BlogNT : fondé en 2010 (tes textes) ou 2011 (CV et page À propos). Que retenir ? Et utiliser les chiffres du site (≈53 000 articles, ≈108 000 lecteurs/mois) ?
3. Quelles coordonnées publier ? (e-mail et LinkedIn figurent dans ton CV ; aucune adresse ni téléphone ne sera affiché.)
4. Quel ton pour les textes ? Et faut-il une version anglaise (ton CV est bilingue, tu travailles sur des projets européens) ?

### Codex
Quatre questions posées en texte libre :
1. Quel rôle doit occuper BlogNT sur la page ?
2. À qui veux-tu surtout t'adresser ?
3. Quels liens souhaites-tu afficher ?
4. As-tu une photo, un logo ou une identité visuelle à utiliser ?

### Lovable
Quatre questions interactives pour la construction (facette dominante, date de création de BlogNT, moyens de contact publics, photo), puis quatre autres pendant la retouche (voir ci-dessous).

## Retouche commune

```
Ajoute une section “Derniers tests” avec 3 cartes (image, titre, note) et rends le titre principal plus percutant.
```

Texte identique vérifié dans les journaux de Claude Code et de Codex, et sur la capture de Lovable.

Questions posées par Lovable pendant la retouche, avec les réponses données :

| Question | Réponse donnée |
| --- | --- |
| Quel contenu pour les 3 cartes « Derniers tests » ? D'où viennent les tests ? | Chercher sur BlogNT |
| Sous quelle forme afficher la note d'un test ? | Note sur 10 |
| Quelles images pour les cartes ? | Images des articles |
| Quelle direction pour le titre principal plus percutant ? | Phrase-choc |

## Relances (motif)

Relances = messages envoyés après le prompt, hors réponses aux questions de l'outil, validation et retouche commune (protocole v1.1).

| Outil | # | Motif |
| --- | --- | --- |
| Claude Code | — | Aucune avant la validation de la page. Après la retouche, le testeur a fourni trois liens parce que les tests choisis n'étaient pas ceux attendus : compté dans la retouche (après relance : 5 points ; les liens du testeur omettaient EA Sports FC 27, voir le README de l'épreuve), pas dans l'autonomie |
| Codex | — | Aucune |
| Lovable | — | Aucune : le fil de conversation ne contient, entre le prompt et la retouche, que les réponses aux questions de l'outil |

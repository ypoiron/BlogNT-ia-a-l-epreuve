# Créer son portfolio sans coder — L'IA à l'épreuve

- **Date du test :** 2026-10-27
- **Protocole :** v1.1
- **Article :** à venir
- **Testeur :** Yohann Poiron

## La tâche

Créer la page d'accueil du portfolio personnel de Yohann Poiron (fondateur de BlogNT, expert en interopérabilité de la santé) à partir de son CV et de recherches publiques : questions de cadrage, direction artistique, page responsive en modes clair et sombre, vérification des liens, de l'accessibilité et du mobile. Une retouche commune est demandée ensuite : ajouter une section « Derniers tests » et rendre le titre principal plus percutant.

Prompt exact et réponses données : [prompt.md](prompt.md).

## Conditions

| Outil | Version | Modèle | Effort | Offre | Prix mensuel |
| --- | --- | --- | --- | --- | --- |
| Claude Code | 2.1.308 | claude-sonnet-5-5 | faible | Pro | 15 € |
| Codex | 0.159.2 | gpt-6-luna | low | Go | 8 € |
| Lovable | non visible | non visible | non visible | Gratuite | 0 € |

## Résultats

Détail complet dans [resultats.csv](resultats.csv). Le coût n'est pas mesuré : le total est sur 90.

| Critère | Claude Code | Codex | Lovable |
| --- | --- | --- | --- |
| Temps (min) | 2,03 | 1,48 | 3,45 |
| Coût (€) | non mesuré | non mesuré | non mesuré |
| Relances | 0 | 0 | 0 |
| Erreurs factuelles | 0 | 0 | 2 |
| Lighthouse mobile (moy.) | 92,0 | 92,0 | 91,3 |
| Design /5 | 4 | 4 | 4 |
| Textes /5 | 4 | 3 | 4 |
| Retouche commune | après relance | 1er coup | échec |
| **Total (sur le maximum indiqué)** | **76,1 / 90** | **81,8 / 90** | **62,0 / 90** |

## Voir les résultats

- Claude Code : [site](https://ypoiron.github.io/BlogNT-ia-a-l-epreuve/epreuves/2026-11-portfolio/claude-code/) · [code](claude-code/index.html) · [captures](claude-code/captures/) · [relevé](claude-code/releve.json)
- Codex : [site](https://ypoiron.github.io/BlogNT-ia-a-l-epreuve/epreuves/2026-11-portfolio/codex/) · [code](codex/index.html) · [captures](codex/captures/) · [relevé](codex/releve.json)
- Lovable : [site](https://yohann-poiron-paper-trail.lovable.app/) · [captures](lovable/captures/) · [relevé](lovable/releve.json)

## Retouche : le standard appliqué

La demande ne précise pas lesquels, mais la retouche est jugée sur « les trois tests les plus récents de BlogNT », avec leurs vraies notes et images : Fitbit Air (12 octobre), Galaxy Z Fold 8 (2 octobre), EA Sports FC 27 (28 septembre). Le même standard s'applique aux trois outils.

- **Codex** a trouvé ces trois tests du premier coup : 10 points.
- **Claude Code** a d'abord retenu un test de 2025 (Honor Magic V5). Le testeur lui a alors fourni trois liens : Fitbit Air, Galaxy Z Fold 8 et Galaxy Watch Ultra 2. **Ces liens omettaient EA Sports FC 27 : c'est une erreur du testeur**, qui aurait dû citer le test du 28 septembre à la place de la Watch Ultra 2 (18 septembre). La page finale reprend fidèlement ces liens. Claude Code n'est pas pénalisé pour cet écart : retouche après relance, 5 points.
- **Lovable** a affiché le Galaxy Watch Ultra 2 à la place du Fitbit Air, tout en annonçant « vos 3 tests les plus récents ». Il n'a pas été relancé : échec, 0 point.

## Erreurs factuelles relevées

- Lovable : une citation de l'entretien Mindalicious 2013 est modifiée entre guillemets ; l'intitulé « Architecte de l'interopérabilité » n'est pas dans le CV (« Expert interopérabilité »).
- Claude Code et Codex : aucune erreur trouvée. Les dates, employeurs, formations et langues ont été comparés au CV ; les cartes de Claude Code sur le Projectathon 2026 et la Journée française de l'interopérabilité 2023 l'ont été aux pages de l'ANS. La carte « FHIR France Meetup #13 » de Claude Code, sans lien, n'a pas pu être vérifiée.

## Mesure du temps

Temps retenu : de l'envoi du prompt au premier message de l'outil annonçant la page disponible, moins mes temps de réponse (horodatages des journaux). Ce repère a été fixé après les tests : les durées selon deux autres repères sont donc publiées.

| Repère | Claude Code | Codex | Lovable |
| --- | --- | --- | --- |
| **Retenu : 1er message annonçant la page** | 2 min 02 s | 1 min 29 s | 3 min 27 s (chronomètre de l'interface) |
| Fichier écrit | 1 min 27 s | 1 min 23 s | non mesurable |
| Fin du tour de l'outil | 2 min 02 s | 21 min 04 s | non mesurable |

- Codex a annoncé « La première version est en place » avant ses contrôles. Un serveur local a ensuite bloqué ses vérifications pendant environ 18,5 minutes, ce qui explique l'écart de la dernière ligne.
- Lovable n'a pas de journal horodaté : sa durée vient du chronomètre affiché dans l'interface.

### Sensibilité au repère de temps

Totaux sur 90 selon le repère retenu pour le temps :

| Repère | Claude Code | Codex | Lovable | Premier |
| --- | --- | --- | --- | --- |
| **Retenu : 1er message annonçant la page** | 76,1 | 81,8 | 62,0 | Codex |
| Fichier écrit | 78,3 | 81,8 | 61,7 | Codex |
| Fin du tour de l'outil | 78,8 | 72,8 | 63,6 | **Claude Code** |

Pour Lovable, la durée n'est mesurable qu'au chronomètre (3 min 27 s), conservée dans les trois lignes. Avec « fin du tour », qui compte les contrôles demandés par le prompt, Claude Code passe devant Codex de 6 points.

## Coût : non mesuré

Les offres testées (Claude Code : Pro ; Codex : Go ; Lovable : gratuite) ne permettent pas de convertir la consommation en euros. Le critère est déclaré non mesuré (protocole v1.1) et le total est calculé sur 90 points. La consommation brute est publiée sans conversion :

| | Consommation relevée |
| --- | --- |
| Claude Code | entrée 60 ; cache écrit 58 214 ; cache lu 2 541 029 ; sortie 22 857 (journal) |
| Codex | entrée 2 987 208 (dont 2 710 144 en cache) ; sortie 13 252 (journal) |
| Lovable | 5,9 crédits (5 couverts par l'enveloppe gratuite) |

Décision prise le 27 octobre 2026, après les tests, sans connaître aucun coût.

## Données personnelles et captures

- L'adresse e-mail de contact des pages produites a été remplacée par une adresse générique (`contact@example.com`) dans les fichiers `index.html` publiés, et masquée par un aplat gris sur les captures où elle apparaissait. Aucune autre modification n'a été apportée aux sites produits. La version en ligne de Lovable n'a pas été modifiée.
- Les captures ont été réduites pour le dépôt : largeur de 1 400 px (700 px en mobile), format JPEG, proportions conservées.

## Limites

- Un seul essai par outil : la variabilité d'un même modèle n'est pas mesurée.
- Lighthouse : mesuré en local pour Claude Code et Codex, et sur la version en ligne pour Lovable, pas avec PageSpeed Insights. Les trois moyennes ne sont donc pas strictement comparables.
- Le prompt n'est pas identique au caractère près : Claude Code a reçu « Mon CV (Profile (1).pdf) est joint dans le dossier » au lieu de « Mon CV est joint ».
- La session Claude Code n'était pas vierge : son journal montre des skills, des instructions MCP et des outils différés chargés.
- Le journal de Lovable est une copie du fil de l'interface, sans horodatage précis ni versions : son relevé combine cette copie et des captures ; les captures mobiles de Claude Code et de Lovable sont tronquées à 16 384 px.
- Les notes des tests (7,8 · 8,5 · 7,5 · 8,6) sont concordantes entre les trois outils ; elles n'ont pas été relues sur les pages.
- L'effort de Codex est celui du journal (`low`).
- Erreur du testeur : les liens fournis à Claude Code pour la retouche omettaient EA Sports FC 27 (voir « Retouche »).
- Les notes de design et de textes sont des notes de testeur.

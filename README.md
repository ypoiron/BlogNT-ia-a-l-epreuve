# L'IA à l'épreuve — BlogNT

Chaque semaine, [BlogNT](https://www.blog-nouvelles-technologies.fr/) confie **une tâche réelle** à **trois outils d'IA**, avec **le même prompt** et **le même protocole**, et publie tout : prompts, réponses, relevés extraits des journaux, sites ou fichiers produits, mesures.

Ce dépôt est la preuve. L'analyse et le verdict sont dans les articles.

## Pourquoi ce dépôt

- **Vérifier** : chaque note est appuyée par une mesure, une capture ou un extrait de journal.
- **Reproduire** : le prompt exact et les réponses données aux questions des outils sont publiés.
- **Comparer dans le temps** : toutes les épreuves utilisent la même grille sur 100 points, ou sur le maximum indiqué si un critère n'est pas mesuré (voir [PROTOCOLE.md](PROTOCOLE.md), « Critère non mesurable », depuis la v1.1).

## Les épreuves

| Date | Tâche | Outils | Gagnant | Score | Article | Dossier |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-27 | Créer son portfolio sans coder | Claude Code · Codex · Lovable | Codex | 81,8 / 90 | _à venir_ | [epreuves/2026-11-portfolio](epreuves/2026-11-portfolio/) |

Gagnant selon le repère de temps retenu. Avec le repère « fin du tour de l'outil », Claude Code passe devant (78,8 contre 72,8) : voir la sensibilité dans le [README de l'épreuve](epreuves/2026-11-portfolio/README.md).

## Classement cumulé

Le fichier [classement.csv](classement.csv) regroupe les résultats de toutes les épreuves (une ligne par outil et par épreuve). Le coût n'étant pas mesuré pour l'épreuve portfolio, ses totaux sont sur 90 et ne se comparent pas directement à un total sur 100.

| Épreuve | Outil | Offre | Temps (min) | Relances | Erreurs | Lighthouse (moy.) | Design /5 | Textes /5 | Retouche | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-portfolio | Codex | Go | 1,48 | 0 | 0 | 92,0 | 4 | 3 | 1er coup | **81,8 / 90** |
| 2026-11-portfolio | Claude Code | Pro | 2,03 | 0 | 0 | 92,0 | 4 | 4 | après relance | **76,1 / 90** |
| 2026-11-portfolio | Lovable | Gratuite | 3,45 | 0 | 2 | 91,3 | 4 | 4 | échec | **62,0 / 90** |

## Structure

```
PROTOCOLE.md                 règles fixes et grille de notation (versionnées)
classement.csv               cumul de toutes les épreuves
epreuves/AAAA-MM-tache/
  README.md                  tâche, conditions, résultats, lien vers l'article
  prompt.md                  prompt exact + réponses données aux questions
  resultats.csv              une ligne par outil
  <outil>/                   site ou fichier produit, releve.json, captures
outils/nettoyer_journaux.py  nettoie les journaux bruts (données sensibles, chemins, identifiants de session) ; ils ne sont pas publiés
outils/extraire_releve.py    relevé extrait du journal (horodatages, tokens, appels d'outils)
_modele-epreuve/             dossier à copier pour chaque nouvelle épreuve
```

Relevé extrait du journal (horodatages, tokens, appels d'outils) ; les journaux complets ne sont pas publiés car ils contiennent l'environnement du testeur.

## Limites assumées

- Les outils évoluent vite : chaque résultat est daté et lié à une version précise.
- Un ou deux essais par outil ne mesurent pas toute la variabilité d'un modèle.
- Les critères design et textes sont des notes de testeur, justifiées par des captures et des citations.

Une erreur, une mesure contestée ? Ouvrez une issue : les corrections sont publiées dans l'article et dans ce dépôt.

## Licence

- Textes, données et captures : [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr) — réutilisation libre en citant « BlogNT — L'IA à l'épreuve ».
- Code généré par les outils et scripts : [MIT](LICENSE).

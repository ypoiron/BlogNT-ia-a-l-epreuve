# Protocole — version 1.3 (octobre 2026)

Toute modification de ce protocole change sa version. Chaque épreuve indique la version utilisée.

- v1.3 : relevé extrait du journal publié (horodatages, tokens, appels d'outils) ; les journaux complets ne sont pas publiés.
- v1.2 : déclaration préalable des choix de mesure ; gamme testée ; méthodes de mesure identiques pour les trois outils ; conditions vérifiées dans le journal ; sensibilité publiée.
- v1.1 : un critère impossible à mesurer de la même façon pour les trois outils est déclaré « non mesuré » ; définition des relances et du temps.
- v1.0 : version initiale.

## Conditions

1. Trois outils dans la même gamme, chacun avec le meilleur modèle disponible dans l'offre testée, noté tel quel (outil, version, modèle, niveau d'effort, offre, prix mensuel). La gamme est déclarée : entrée de gamme (offre gratuite ou premier palier payant) ou haut de gamme (offre la plus élevée accessible au public).
2. Sessions vierges : dossier vide, aucun fichier d'instructions hérité (`CLAUDE.md`, `AGENTS.md`, règles de projet). Vérifié dans le journal : aucun skill, serveur MCP, instruction ni mémoire chargé. Sinon, l'écart est déclaré dans les limites.
3. Prompt identique au caractère près, vérifié en comparant les journaux ; pièces jointes fournies de la même façon. Réponses aux questions des outils rédigées une fois, réutilisées mot pour mot. Si les outils posent des questions différentes, les réponses sont données au fil de l'eau et publiées.
4. Écran enregistré du collage du prompt jusqu'au résultat final.
5. Même retouche finale demandée à chaque outil (critère « modifiabilité »). Son critère de réussite est déclaré avant l'épreuve.
6. Mêmes méthodes de mesure pour les trois outils (Lighthouse notamment). Tout écart est déclaré dans les limites.

## Déclaration préalable

Avant le premier test, le testeur renseigne dans le README de l'épreuve, avec la date :

- la gamme testée, et les offres, modèles et niveaux d'effort ;
- le critère de réussite de la retouche commune ;
- la méthode Lighthouse (URL publique ou local) ;
- les critères qu'il prévoit de ne pas mesurer.

Tout choix fait ou modifié après avoir vu un résultat est déclaré comme tel, et sa sensibilité est publiée (voir « Publication »).

## Grille sur 100 points

| Critère | Mesure | Relevé | Points |
| --- | --- | --- | --- |
| Temps | Minutes jusqu'au premier message de l'outil annonçant la page disponible, hors temps de réponse du testeur | Horodatages du journal (prompt → premier message annonçant la page, moins les attentes du testeur) ; à défaut, chronomètre de l'outil ou enregistrement | 10 |
| Coût | Tokens ou crédits convertis en euros au prorata de l'offre (« non mesuré » si la conversion est impossible) | Compteur de l'outil, solde avant/après | 10 |
| Autonomie | Relances du testeur après le prompt, hors réponses aux questions de l'outil, validation et retouche commune | Journal ; à défaut, comptage manuel | 15 |
| Exactitude | Erreurs factuelles et éléments inventés | Relecture ligne à ligne contre les sources de référence de l'épreuve : −3 points par erreur. Une même défaillance n'est comptée qu'une fois (exactitude ou modifiabilité) | 15 |
| Qualité technique | Moyenne Lighthouse mobile (performance, accessibilité, SEO) | PageSpeed Insights sur l'URL publique ; à défaut, Lighthouse en local pour les trois outils | 15 |
| Design | 1 à 5 : lisibilité, identité, mobile, cohérence | Note justifiée par captures | 15 |
| Textes | 1 à 5 : justesse, personnalité, absence de clichés | Note justifiée par citations | 10 |
| Modifiabilité | Retouche commune : 1er coup = 10, après relance = 5, échec = 0 | Journal ; critère de réussite déclaré avant l'épreuve | 10 |

### Conversion en points

- **Temps et coût** : le meilleur outil obtient le maximum ; les autres au prorata (`max × meilleur / valeur`).
- **Autonomie** : 15 − 3 par relance (minimum 0).
- **Exactitude** : 15 − 3 par erreur (minimum 0).
- **Qualité technique** : `15 × moyenne Lighthouse / 100`.
- **Design** : `15 × note / 5`. **Textes** : `10 × note / 5`.

## Critère non mesurable

Un critère n'est noté que s'il se mesure de la même façon pour les trois outils. Pour le coût, c'est le cas quand chaque offre permet de convertir la consommation en euros. Sinon :

- le critère est déclaré « non mesuré », avec la raison (offre gratuite, forfait sans compteur de consommation) ;
- la consommation brute est publiée telle que relevée (tokens, crédits, capture du compteur), sans conversion ni estimation ;
- aucun point n'est attribué ni redistribué : le total est calculé sur les points restants (par exemple 90) et son maximum est indiqué à côté de chaque score ;
- les totaux de maximum différent ne se comparent pas directement.

La décision tient à la nature des offres, jamais aux résultats. Elle est datée dans le README de l'épreuve.

## Questions posées par l'outil

Comptées, puis notées de 1 à 5 :

- 5 : chaque question a modifié le résultat ;
- 3 : la moitié est utile, l'autre porte sur des informations déjà fournies ;
- 1 : questions génériques ou déjà répondues.

Information publiée, hors score.

## Sources consultées

Nombre de recherches et de pages lues, avec 2 ou 3 exemples. « Non visible » si l'outil ne les expose pas. Information publiée, hors score.

## Publication

- Les journaux bruts ne sont jamais commités : ils restent dans un dossier `brut/`, ignoré par git.
- On publie un relevé extrait du journal (horodatages des étapes, tokens par tour, noms et nombre d'appels d'outils, domaines consultés, noms des fichiers écrits), produit par `outils/extraire_releve.py` : aucun texte de message, aucun chemin local. Les journaux complets ne sont pas publiés car ils contiennent l'environnement du testeur. Le relevé est relu avant tout commit. Pour un outil sans journal technique (copie du fil de l'interface), il est établi à partir de cette copie et de captures, et le signale.
- Les captures sont réduites pour le dépôt (1 400 px de large, 700 px en mobile, JPEG).
- Les données personnelles des sites produits (adresse e-mail de contact, par exemple) sont remplacées par une valeur générique et masquées sur les captures ; le README de l'épreuve le déclare.
- Pour le temps, les durées mesurées à l'écriture du fichier et à la fin du tour de l'outil sont publiées à titre de sensibilité, avec les totaux correspondants. Si un autre repère défendable change le premier, l'article le dit.
- Aucune donnée privée (adresse, téléphone, clés, chemins locaux).
- Liens d'affiliation éventuels signalés dans l'article ; aucun éditeur ne voit les résultats avant publication.

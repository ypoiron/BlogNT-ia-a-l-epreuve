# Contexte — L'IA à l'épreuve (BlogNT)

BlogNT (blog-nouvelles-technologies.fr) est un média tech indépendant tenu par Yohann Poiron.
« L'IA à l'épreuve » : une tâche réelle, 3 outils IA, même prompt, protocole fixe (PROTOCOLE.md), score /100.
Ce dépôt est la preuve publique ; l'article sur BlogNT porte l'analyse. https://github.com/ypoiron/BlogNT-ia-a-l-epreuve

## Règles non négociables
- Tout chiffre de l'article vient de resultats.csv ou d'une fiche de relevé. Jamais d'estimation présentée comme une mesure.
- L'article est écrit au « je » UNIQUEMENT pour ce que Yohann a fait lui-même. Toute source externe est citée nommément.
- Les journaux bruts (*.raw.jsonl, brut/) ne sont jamais commités. Toujours passer par outils/nettoyer_journaux.py, puis afficher un extrait pour relecture avant commit.
- WordPress : créer ou mettre à jour en statut "draft" uniquement. Ne jamais publier, ne jamais modifier un article publié.
- Catégorie WordPress : Intelligence artificielle (ID à récupérer via l'API). Série : ia-a-l-epreuve (ID à récupérer via l'API). Ne jamais créer de catégorie ni de série.
- Ne jamais afficher, écrire ou committer les identifiants (WP_USER, WP_APP_PASSWORD).

## Flux d'une épreuve
0. Avant tout test : la « Déclaration préalable » du README de l'épreuve est renseignée et datée (protocole v1.3).
1. Lire epreuves/<epreuve>/fiches/*.md (fiches de relevé) et les relevés (outils/extraire_releve.py). Les journaux complets restent dans brut/ et ne sont pas publiés.
2. Calculer les points selon PROTOCOLE.md, remplir resultats.csv, ajouter les lignes à classement.csv.
3. Remplir epreuves/<epreuve>/README.md et le tableau du README racine.
4. Rédiger l'article selon le gabarit (ci-dessous), l'enregistrer dans epreuves/<epreuve>/article.md.
5. Montrer le diff, attendre validation, puis commit + push.
6. Envoyer l'article en brouillon WordPress via l'API REST, catégorie « Intelligence artificielle » et série « L'IA à l'épreuve », et donner le lien d'édition.

## Gabarit d'article
Titre « [Tâche] : A, B ou C ? On a mesuré » · chapô 2 phrases avec le gagnant et son score · encadré En bref ·
La tâche · Le protocole · Tableau des résultats · Une section par outil (captures) · Verdict par profil ·
Ce qu'on n'a pas pu tester · Annexes (prompt, lien GitHub).
Ton : direct, « on tranche », phrases courtes, pas de superlatifs non mesurés.

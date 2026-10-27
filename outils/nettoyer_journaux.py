#!/usr/bin/env python3
"""Nettoie les journaux .jsonl (Claude Code, Codex) avant publication.

Usage :
    # journal nettoyé (même structure, données sensibles masquées)
    python3 outils/nettoyer_journaux.py journal.jsonl -o journal-nettoye.jsonl \
        --masquer "06 12 34 56 78" --masquer "12 rue Exemple"

    # transcript lisible de la conversation (recommandé pour la publication)
    python3 outils/nettoyer_journaux.py journal.jsonl --transcript transcript.md \
        --outil "Claude Code"

Ce que fait le script :
- masque e-mails, numéros de téléphone FR, clés d'API et jetons courants ;
- remplace les chemins locaux (/Users/nom, /home/nom, C:\\Users\\nom) par ~ ;
- masque les chemins encodés avec des tirets (-Users-<nom>-…) et les identifiants de session ;
- masque les chaînes passées avec --masquer (adresse, nom de client, etc.) ;
- supprime les blocs d'images base64 (captures collées) ;
- affiche un résumé : tokens, recherches web, pages lues, messages du testeur.

Le transcript ne contient que : les messages du testeur, les réponses de l'outil,
ses questions et les réponses qui leur sont données, et un résumé de chaque appel
d'outil (recherche, page, fichier, commande). Il omet les prompts système, les pièces
jointes d'environnement (instructions, outils, mémoire), le raisonnement et les
résultats d'outils. Formats reconnus : Claude Code et Codex.

Relisez TOUJOURS le résultat avant de le publier : aucun filtre n'est parfait.
"""
import argparse
import json
import re
import sys

MOTIFS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "[CLE_ANTHROPIC]"),
    (re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}"), "[CLE_OPENAI]"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"), "[JETON_GITHUB]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[CLE_AWS]"),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-]{20,}"), r"\1[JETON]"),
    (re.compile(r"(?i)((?:api[_-]?key|token|secret|password)\"?\s*[:=]\s*\"?)[^\s\",]{8,}"), r"\1[SECRET]"),
    (re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"), "[EMAIL]"),
    (re.compile(r"(?<!\d)(?:\+33\s?|0)[1-9](?:[\s.\-]?\d{2}){4}(?!\d)"), "[TELEPHONE]"),
    (re.compile(r"/Users/[^/\s\"]+"), "~"),
    (re.compile(r"/home/[^/\s\"]+"), "~"),
    (re.compile(r"[A-Za-z]:\\\\?Users\\\\?[^\\\s\"]+"), "~"),
    # chemins encodés avec des tirets (dossiers de projets, p. ex. -Users-<nom>-www-projet)
    (re.compile(r"-(?:Users|home)-[A-Za-z0-9_.\-]+"), "[CHEMIN_ENCODE]"),
    # identifiants de session, de tour et de rollout (UUID, sess_..., session-...)
    (re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"), "[ID_SESSION]"),
    (re.compile(r"(?i)\b(?:sess|session)[_-][A-Za-z0-9_-]{8,}"), "[ID_SESSION]"),
]

EXCEPTIONS_EMAIL = {"noreply@anthropic.com"}
LONGUEUR_RESUME = 160


def nettoyer_texte(texte, masques):
    for chaine in masques:
        texte = texte.replace(chaine, "[MASQUE]")
    for motif, remplacement in MOTIFS:
        if remplacement == "[EMAIL]":
            texte = motif.sub(
                lambda m: m.group(0) if m.group(0) in EXCEPTIONS_EMAIL else "[EMAIL]", texte
            )
        else:
            texte = motif.sub(remplacement, texte)
    return texte


def nettoyer(objet, masques):
    if isinstance(objet, dict):
        # « source » est parfois une chaîne (et non un objet) selon les formats
        source = objet.get("source")
        source = source if isinstance(source, dict) else {}
        if objet.get("type") == "image" or "base64" in str(source.get("type", "")):
            return {"type": "image", "note": "[image supprimée]"}
        return {k: nettoyer(v, masques) for k, v in objet.items()}
    if isinstance(objet, list):
        return [nettoyer(v, masques) for v in objet]
    if isinstance(objet, str):
        return nettoyer_texte(objet, masques)
    return objet


def format_codex(lignes):
    return any(l.get("type") in ("response_item", "turn_context", "event_msg") for l in lignes)


def court(texte, n=LONGUEUR_RESUME):
    texte = " ".join(str(texte).split())
    return texte if len(texte) <= n else texte[: n - 1] + "…"


def textes(contenu):
    if isinstance(contenu, str):
        return [contenu]
    if isinstance(contenu, list):
        return [x.get("text", "") for x in contenu
                if isinstance(x, dict) and x.get("type") in ("text", "input_text", "output_text")]
    return []


def message_testeur(texte):
    """Garde uniquement ce que le testeur a écrit (pas les blocs injectés par l'application)."""
    if "## My request:" in texte:
        texte = texte.split("## My request:", 1)[1]
    texte = texte.strip()
    if not texte or texte.startswith("<") or texte.startswith("[Request interrupted"):
        return ""
    return texte


# --- Claude Code -----------------------------------------------------------

def resume_outil_cc(bloc):
    nom, entree = bloc.get("name", "outil"), bloc.get("input") or {}
    if nom == "AskUserQuestion":
        return None
    for cle in ("query", "url", "file_path", "command", "description", "pattern", "skill"):
        if entree.get(cle):
            return f"{nom} — {court(entree[cle])}"
    return nom


def extraire_cc(lignes):
    for d in lignes:
        heure, msg, typ = d.get("timestamp", "")[11:19], d.get("message"), d.get("type")
        if not isinstance(msg, dict):
            continue
        contenu = msg.get("content")
        if typ == "user":
            for t in textes(contenu):
                t = message_testeur(t)
                if t:
                    yield heure, "testeur", t
            for x in contenu if isinstance(contenu, list) else []:
                if isinstance(x, dict) and x.get("type") == "tool_result":
                    brut = x.get("content")
                    s = brut if isinstance(brut, str) else " ".join(textes(brut))
                    if "have been answered" in s:
                        yield heure, "reponses", re.findall(r'"([^"]+)"="([^"]*)"', s)
        elif typ == "assistant" and isinstance(contenu, list):
            for x in contenu:
                if not isinstance(x, dict):
                    continue
                if x.get("type") == "text" and x.get("text", "").strip():
                    yield heure, "outil_texte", x["text"].strip()
                elif x.get("type") == "tool_use":
                    if x.get("name") == "AskUserQuestion":
                        qs = (x.get("input") or {}).get("questions", [])
                        yield heure, "questions", [
                            (q.get("question", ""), [o.get("label", "") for o in q.get("options", [])])
                            for q in qs]
                    else:
                        r = resume_outil_cc(x)
                        if r:
                            yield heure, "appel", r


def usage_cc(lignes):
    """Dernier relevé d'usage de chaque message (un message est écrit en plusieurs lignes)."""
    par_id = {}
    for d in lignes:
        m = d.get("message")
        if d.get("type") == "assistant" and isinstance(m, dict) and m.get("usage"):
            par_id[m.get("id") or d.get("uuid")] = m["usage"]
    t = dict(entree=0, cache_ecrit=0, cache_lu=0, sortie=0)
    for u in par_id.values():
        t["entree"] += u.get("input_tokens", 0)
        t["cache_ecrit"] += u.get("cache_creation_input_tokens", 0)
        t["cache_lu"] += u.get("cache_read_input_tokens", 0)
        t["sortie"] += u.get("output_tokens", 0)
    return t


# --- Codex -----------------------------------------------------------------

def resume_exec_codex(code):
    if "web__run" in code:
        requetes = re.findall(r'\bq:\s*"((?:[^"\\]|\\.)*)"', code) + re.findall(r'"q"\s*:\s*"((?:[^"\\]|\\.)*)"', code)
        requetes = [q.replace('\\"', '"') for q in requetes]
        pages = re.findall(r'ref_id\s*:\s*"(https?://[^"]+)"', code)
        morceaux = []
        if requetes:
            morceaux.append("recherche : " + " | ".join(requetes))
        if pages:
            morceaux.append("page : " + ", ".join(pages))
        return "web — " + (" ; ".join(morceaux) if morceaux else "ouverture ou clic sur un résultat")
    fichiers = re.findall(r'\*\*\* (Add|Update|Delete) File: ([^\\"]+)', code)
    if fichiers:
        return "fichier — " + ", ".join(f"{a} {f}" for a, f in fichiers)
    m = re.search(r'cmd\s*:\s*"((?:[^"\\]|\\.)*)"', code)
    if m:
        return "commande — " + court(m.group(1).replace('\\"', '"'))
    return "exec"


def extraire_codex(lignes):
    for d in lignes:
        heure, p = d.get("timestamp", "")[11:19], d.get("payload") or {}
        if d.get("type") != "response_item":
            continue
        typ = p.get("type")
        if typ == "message":
            if p.get("role") == "user":
                for t in textes(p.get("content")):
                    t = message_testeur(t)
                    if t:
                        yield heure, "testeur", t
            elif p.get("role") == "assistant":
                t = " ".join(textes(p.get("content"))).strip()
                if t:
                    yield heure, "outil_texte", t
        elif typ == "custom_tool_call":
            yield heure, "appel", resume_exec_codex(p.get("input") or "")
        elif typ == "function_call":
            try:
                args = json.loads(p.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            if p.get("name") == "wait":
                yield heure, "appel", "attente d'une commande en cours"
            else:
                yield heure, "appel", f"{p.get('name', 'outil')} — {court(args.get('title') or '')}".rstrip(" —")


def usage_codex(lignes):
    dernier = {}
    for d in lignes:
        p = d.get("payload") or {}
        info = p.get("info") if p.get("type") == "token_count" else None
        if isinstance(info, dict) and info.get("total_token_usage"):
            dernier = info["total_token_usage"]
    entree, cache = dernier.get("input_tokens", 0), dernier.get("cached_input_tokens", 0)
    return dict(entree=entree - cache, cache_ecrit=dernier.get("cache_write_input_tokens", 0),
                cache_lu=cache, sortie=dernier.get("output_tokens", 0))


# --- Sorties ---------------------------------------------------------------

def citation(texte):
    return "\n".join("> " + l if l.strip() else ">" for l in texte.strip().splitlines())


def ecrire_transcript(entrees, chemin, outil, masques):
    n = lambda t: nettoyer_texte(t, masques)
    sorties = [f"# Transcript — {outil}\n",
               "Conversation extraite du journal de la session, nettoyée avant publication. "
               "Heures en UTC (Paris = UTC+1 à cette date).\n",
               "Ne sont pas publiés : prompts système, pièces jointes d'environnement, raisonnement "
               "et résultats des outils. Chaque appel d'outil est résumé en une ligne.\n"]
    appels = False
    for heure, genre, valeur in entrees:
        if genre == "appel":
            sorties.append(("" if appels else "\n") + f"- `{heure}` {n(valeur)}")
            appels = True
            continue
        appels = False
        if genre == "testeur":
            sorties.append(f"\n### {heure} · Testeur\n\n{n(citation(valeur))}")
        elif genre == "outil_texte":
            sorties.append(f"\n### {heure} · {outil}\n\n{n(citation(valeur))}")
        elif genre == "questions":
            lignes = [f"{i}. {q}  \n   Choix proposés : {' · '.join(o) if o else 'réponse libre'}"
                      for i, (q, o) in enumerate(valeur, 1)]
            sorties.append(f"\n### {heure} · {outil} pose des questions\n\n{n(chr(10).join(lignes))}")
        elif genre == "reponses":
            lignes = [f"- {q} → **{r}**" for q, r in valeur]
            sorties.append(f"\n### {heure} · Réponses du testeur\n\n{n(chr(10).join(lignes))}")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(sorties).rstrip() + "\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entree")
    p.add_argument("-o", "--sortie", help="journal .jsonl nettoyé")
    p.add_argument("--transcript", help="transcript Markdown de la conversation")
    p.add_argument("--outil", default="Outil", help="nom affiché dans le transcript")
    p.add_argument("--masquer", action="append", default=[], help="chaîne à masquer (répétable)")
    a = p.parse_args()
    if not a.sortie and not a.transcript:
        p.error("indiquez -o et/ou --transcript")

    lignes, lignes_ko = [], 0
    with open(a.entree, encoding="utf-8") as fe:
        for brute in fe:
            brute = brute.strip()
            if not brute:
                continue
            try:
                lignes.append(json.loads(brute))
            except json.JSONDecodeError:
                lignes_ko += 1

    codex = format_codex(lignes)
    entrees = list(extraire_codex(lignes) if codex else extraire_cc(lignes))
    usage = usage_codex(lignes) if codex else usage_cc(lignes)

    if a.sortie:
        with open(a.sortie, "w", encoding="utf-8") as fs:
            for ligne in lignes:
                fs.write(json.dumps(nettoyer(ligne, a.masquer), ensure_ascii=False) + "\n")
    if a.transcript:
        ecrire_transcript(entrees, a.transcript, a.outil, a.masquer)

    appels = [v for _, g, v in entrees if g == "appel"]
    recherches = sum(v.count(" | ") + 1 for v in appels if v.startswith("web — recherche")) if codex else \
        sum(1 for v in appels if v.startswith("WebSearch"))
    pages = sum(1 for v in appels if v.startswith("web — page") or v.startswith("WebFetch"))
    print("Résumé (indicatif, à vérifier) :")
    print(f"  format : {'Codex' if codex else 'Claude Code'}")
    print(f"  tokens : entrée {usage['entree']} ; cache écrit {usage['cache_ecrit']} ; "
          f"cache lu {usage['cache_lu']} ; sortie {usage['sortie']}")
    print(f"  messages du testeur : {sum(1 for _, g, _ in entrees if g == 'testeur')}")
    print(f"  recherches web : {recherches} ; pages lues : {pages}")
    if lignes_ko:
        print(f"  lignes non JSON ignorées : {lignes_ko}", file=sys.stderr)
    print("Relisez le résultat avant publication.")


if __name__ == "__main__":
    main()

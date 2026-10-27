#!/usr/bin/env python3
"""Extrait d'un journal de session un relevé publiable (releve.json).

Usage :
    python3 outils/extraire_releve.py journal.jsonl -o releve.json --outil "Claude Code"
    python3 outils/extraire_releve.py journal.log   -o releve.json --outil "Lovable" \
        --etape "10:05=prompt" --etape "10:22=retouche" --credits "5,9 crédits"

Le relevé contient UNIQUEMENT :
- les horodatages des étapes de chaque tour (début, questions, réponses, premier fichier
  écrit, premier message de l'outil après l'écriture, fin) ;
- les tokens de chaque tour ;
- les noms et le nombre d'appels d'outils ;
- les domaines consultés (sans chemin ni paramètres) ;
- les fichiers écrits (nom seul, sans dossier).

Il ne contient aucun texte de message, aucun chemin local, aucune adresse. Les journaux
complets ne sont pas publiés : ils contiennent l'environnement du testeur.

Formats reconnus : Claude Code (.jsonl), Codex (.jsonl), et la copie texte du fil de
Lovable (.log), qui n'a ni horodatage ni tokens (voir --etape et --credits).
Heures en UTC pour Claude Code et Codex.
"""
import argparse
import collections
import json
import os
import re
import sys
from urllib.parse import urlparse

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nettoyer_journaux import format_codex, message_testeur, textes  # noqa: E402

HOTES_LOCAUX = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}
OUTILS_ECRITURE_CC = {"Write", "Edit", "NotebookEdit"}
URL = re.compile(r"https?://[^\s\"'<>)\\]+")


def domaines(texte):
    trouves = []
    for u in URL.findall(texte or ""):
        h = (urlparse(u).hostname or "").lower()
        if h and h not in HOTES_LOCAUX:
            trouves.append(h[4:] if h.startswith("www.") else h)
    return trouves


def nom_fichier(chemin):
    return os.path.basename(str(chemin).replace("\\", "/").rstrip("/"))


def jetons(usage):
    return dict(entree=usage.get("entree", 0), cache_ecrit=usage.get("cache_ecrit", 0),
                cache_lu=usage.get("cache_lu", 0), sortie=usage.get("sortie", 0))


def nouveau_tour(n, debut):
    return {"n": n, "debut": debut, "premier_appel_outil": None, "questions_posees": None,
            "reponses_recues": None, "premier_fichier_ecrit": None,
            "premier_message_apres_ecriture": None, "fin": debut,
            "tokens": dict(entree=0, cache_ecrit=0, cache_lu=0, sortie=0),
            "nb_appels": 0, "appels_par_outil": collections.Counter()}


def finaliser(tours, domaines_vus, fichiers, outil, fmt, fuseau):
    total = dict(entree=0, cache_ecrit=0, cache_lu=0, sortie=0)
    appels = collections.Counter()
    for t in tours:
        for k in total:
            total[k] += t["tokens"][k]
        appels.update(t["appels_par_outil"])
        t["appels_par_outil"] = dict(sorted(t["appels_par_outil"].items()))
    return {"outil": outil, "format": fmt, "fuseau": fuseau, "tours": tours,
            "totaux": {"tokens": total, "nb_appels": sum(appels.values()),
                       "appels_par_outil": dict(sorted(appels.items()))},
            "domaines_consultes": dict(sorted(domaines_vus.items(), key=lambda x: (-x[1], x[0]))),
            "domaines_perimetre": "pages ouvertes par l'outil (lecture de pages, commandes, ouvertures) ; "
                                  "les domaines des résultats de recherche ne sont pas inclus",
            "fichiers_ecrits": dict(sorted(fichiers.items()))}


# --- Claude Code -----------------------------------------------------------

def releve_cc(lignes, outil):
    tours, cur, par_id = [], None, {}
    doms, fichiers = collections.Counter(), collections.Counter()
    for d in lignes:
        ts, msg, typ = d.get("timestamp", "")[11:19], d.get("message"), d.get("type")
        if not isinstance(msg, dict):
            continue
        contenu = msg.get("content")
        if typ == "user":
            if any(message_testeur(t) for t in textes(contenu)):
                cur = nouveau_tour(len(tours) + 1, ts)
                tours.append(cur)
            for x in contenu if isinstance(contenu, list) else []:
                if isinstance(x, dict) and x.get("type") == "tool_result" and cur:
                    brut = x.get("content")
                    s = brut if isinstance(brut, str) else " ".join(textes(brut))
                    if "have been answered" in s:
                        cur["reponses_recues"] = ts
        elif typ == "assistant" and cur is not None and isinstance(contenu, list):
            cur["fin"] = ts
            if msg.get("usage"):
                par_id[msg.get("id") or d.get("uuid")] = (cur["n"] - 1, msg["usage"])
            for x in contenu:
                if not isinstance(x, dict):
                    continue
                if x.get("type") == "text" and x.get("text", "").strip():
                    if cur["premier_fichier_ecrit"] and not cur["premier_message_apres_ecriture"]:
                        cur["premier_message_apres_ecriture"] = ts
                elif x.get("type") == "tool_use":
                    nom, entree = x.get("name", "outil"), x.get("input") or {}
                    cur["nb_appels"] += 1
                    cur["appels_par_outil"][nom] += 1
                    cur["premier_appel_outil"] = cur["premier_appel_outil"] or ts
                    if nom == "AskUserQuestion":
                        cur["questions_posees"] = cur["questions_posees"] or ts
                    if nom in OUTILS_ECRITURE_CC and entree.get("file_path"):
                        fichiers[nom_fichier(entree["file_path"])] += 1
                        cur["premier_fichier_ecrit"] = cur["premier_fichier_ecrit"] or ts
                    if nom == "WebFetch":
                        doms.update(domaines(entree.get("url")))
                    elif nom == "Bash":
                        doms.update(domaines(entree.get("command")))
    for i, u in par_id.values():
        t = tours[i]["tokens"]
        t["entree"] += u.get("input_tokens", 0)
        t["cache_ecrit"] += u.get("cache_creation_input_tokens", 0)
        t["cache_lu"] += u.get("cache_read_input_tokens", 0)
        t["sortie"] += u.get("output_tokens", 0)
    return finaliser(tours, doms, fichiers, outil, "claude-code", "UTC")


# --- Codex -----------------------------------------------------------------

def releve_codex(lignes, outil):
    tours, cur, prec = [], None, dict(input_tokens=0, cached_input_tokens=0, output_tokens=0)
    dernier = dict(prec)
    doms, fichiers = collections.Counter(), collections.Counter()
    for d in lignes:
        ts, p, typ = d.get("timestamp", "")[11:19], d.get("payload") or {}, d.get("type")
        if typ == "event_msg":
            if p.get("type") == "task_started":
                cur = nouveau_tour(len(tours) + 1, ts)
                tours.append(cur)
            elif p.get("type") == "task_complete" and cur:
                cur["fin"] = ts
                e = dernier["input_tokens"] - prec["input_tokens"]
                c = dernier["cached_input_tokens"] - prec["cached_input_tokens"]
                cur["tokens"] = dict(entree=e - c, cache_ecrit=0, cache_lu=c,
                                     sortie=dernier["output_tokens"] - prec["output_tokens"])
                prec = dict(dernier)
            elif p.get("type") == "token_count" and isinstance(p.get("info"), dict):
                u = p["info"].get("total_token_usage")
                if u:
                    dernier = dict(input_tokens=u.get("input_tokens", 0),
                                   cached_input_tokens=u.get("cached_input_tokens", 0),
                                   output_tokens=u.get("output_tokens", 0))
            continue
        if typ != "response_item" or cur is None:
            continue
        nature = p.get("type")
        if nature == "message" and p.get("role") == "assistant" and " ".join(textes(p.get("content"))).strip():
            if cur["premier_fichier_ecrit"] and not cur["premier_message_apres_ecriture"]:
                cur["premier_message_apres_ecriture"] = ts
        elif nature in ("custom_tool_call", "function_call"):
            nom = p.get("name", "outil")
            cur["nb_appels"] += 1
            cur["appels_par_outil"][nom] += 1
            cur["premier_appel_outil"] = cur["premier_appel_outil"] or ts
            code = p.get("input") or p.get("arguments") or ""
            doms.update(domaines(code))
            for _, chemin in re.findall(r'\*\*\* (Add|Update) File: ([^\\"\n]+)', code):
                fichiers[nom_fichier(chemin)] += 1
                cur["premier_fichier_ecrit"] = cur["premier_fichier_ecrit"] or ts
    return finaliser(tours, doms, fichiers, outil, "codex", "UTC")


# --- Lovable (copie texte du fil de l'interface) -----------------------------

def releve_lovable(texte, outil, etapes, credits, manuel):
    lignes = [l.strip() for l in texte.splitlines() if l.strip()]
    appels, fichiers, reflexion = collections.Counter(), collections.Counter(), 0
    for i, l in enumerate(lignes):
        m = re.match(r"Réflexion pendant (\d+)s", l)
        if m:
            reflexion += int(m.group(1))
        elif l == "Searched the web":
            appels["recherche web"] += 1
        elif l == "Commande exécutée":
            appels["commande"] += 1
        elif l == "Questions answered":
            appels["questions posées (série)"] += 1
        elif l == "Modifié" and i + 1 < len(lignes):
            appels["modification de fichier"] += 1
            fichiers[nom_fichier(lignes[i + 1])] += 1
    return {"outil": outil, "format": "lovable (copie texte du fil de l'interface)",
            "fuseau": "heure de Paris, telle qu'affichée par l'interface",
            "etapes": etapes, "tokens": "non visible", "credits": credits or "non précisé",
            "reflexion_cumulee_s": reflexion,
            "totaux": {"nb_appels": sum(appels.values()), "appels_par_nature": dict(sorted(appels.items()))},
            "domaines_consultes": "non visible",
            "fichiers_ecrits": dict(sorted(fichiers.items())),
            "saisi_manuellement": manuel,
            "avertissement": "copie partielle du fil : sans horodatage ni détail des pages consultées ; "
                             "les champs de « saisi_manuellement » viennent de captures, pas de la copie"}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entree")
    p.add_argument("-o", "--sortie", required=True)
    p.add_argument("--outil", required=True)
    p.add_argument("--etape", action="append", default=[], help="HH:MM=nom (formats sans horodatage)")
    p.add_argument("--credits", help="consommation affichée par l'outil (formats sans tokens)")
    p.add_argument("--manuel", action="append", default=[], help="clé=valeur relevée sur une capture (formats .log)")
    a = p.parse_args()

    if a.entree.endswith(".log"):
        texte = open(a.entree, encoding="utf-8").read()
        etapes = [dict(zip(("heure", "etape"), e.split("=", 1))) for e in a.etape]
        manuel = dict(m.split("=", 1) for m in a.manuel)
        releve = releve_lovable(texte, a.outil, etapes, a.credits, manuel)
    else:
        lignes = []
        with open(a.entree, encoding="utf-8") as f:
            for brute in f:
                try:
                    lignes.append(json.loads(brute))
                except json.JSONDecodeError:
                    pass
        releve = (releve_codex if format_codex(lignes) else releve_cc)(lignes, a.outil)
    with open(a.sortie, "w", encoding="utf-8") as f:
        json.dump(releve, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{a.sortie} écrit ({releve['totaux']['nb_appels']} appels d'outils)")


if __name__ == "__main__":
    main()

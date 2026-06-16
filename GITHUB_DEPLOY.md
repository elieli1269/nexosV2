# Déploiement sur GitHub

Ce document explique comment créer le dépôt GitHub `nexosnexaibuild`, pousser le code et activer GitHub Actions (workflow CI fourni).

Prérequis
- `git` installé
- `gh` (GitHub CLI) installé et authentifié (`gh auth login`)
- (Optionnel) `python3` si vous voulez tester localement

Commandes rapides (bash)

```bash
# depuis le dossier racine du projet
chmod +x scripts/create_repo_and_push.sh
./scripts/create_repo_and_push.sh nexosnexaibuild
```

Commandes rapides (PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\create_repo_and_push.ps1 -Repo "nexosnexaibuild"
```

Que fait le workflow CI?
- Vérifie la présence de `nexos-live/index.html`
- Vérifie la syntaxe Python de `nexos-backend.py`

Notes de sécurité
- Le backend local (`nexos-backend.py`) écoute sur `127.0.0.1:9876` et appelle `/usr/local/bin/nexos uninstall` lorsque l'UI déclenche la désinstallation. Assurez-vous que la commande `nexos uninstall` ne supprime que les éléments prévus.

Si tu veux, je peux initier le `git commit` et te fournir les commandes exactes pour créer le repo via `gh` depuis ton poste (je ne peux pas créer le repo distant sans ton compte/jeton local).
#!/usr/bin/env bash
set -e

REPO_NAME=${1:-nexosnexaibuild}

if ! command -v gh >/dev/null 2>&1; then
  echo "Erreur: GitHub CLI 'gh' introuvable. Installez-la d'abord: https://cli.github.com/"
  exit 1
fi

if [ ! -d .git ]; then
  git init
fi

git add .
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git commit -m "Initial commit: NEXOS + backend + CI"
else
  git commit -m "Update" || true
fi

# create repo and push
gh repo create "$REPO_NAME" --public --source=. --remote=origin --push

echo "Repository https://github.com/$(gh api user --jq .login)/$REPO_NAME créé et push effectué (si autorisé)."
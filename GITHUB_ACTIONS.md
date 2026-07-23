# GitHub Actions CI/CD pour Nexos ISO

## Vue d'ensemble

Ce projet utilise GitHub Actions pour construire automatiquement l'image ISO Nexos bootable.

## Workflow disponible

### Build Nexos Live ISO (`build-nexos-iso.yml`)

**Déclenché par :**
- Commits sur `main` ou `develop`
- Pull requests sur `main` ou `develop`
- Changements dans le dossier `nexos-live/`
- Manuel via `workflow_dispatch`

**Étapes :**
1. ✅ Vérifie le code source
2. ✅ Installe les dépendances (live-build, debootstrap)
3. ✅ Valide les fichiers requis
4. ✅ Construit l'ISO Debian Live
5. ✅ Génère les checksums SHA256
6. ✅ Upload l'ISO en tant qu'artifact
7. ✅ Crée une release si c'est un tag

**Temps de build :** 15-20 minutes

## Utilisation

### Déclencher un build manuellement

```bash
gh workflow run build-nexos-iso.yml -r main
```

### Télécharger l'ISO depuis les artifacts

1. Allez sur [Actions](https://github.com/elieli1269/nexosV2/actions)
2. Sélectionnez la dernière exécution de "Build Nexos Live ISO"
3. Téléchargez l'artifact `nexos-iso-main`

### Créer une release

Créez un tag pour automatiquement générer une release avec l'ISO :

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Dépannage

### Build échoue avec "Package not found"

**Problème :** Un paquet listé dans `nexos.list.chroot` n'existe pas.

**Solution :**
1. Vérifiez que le paquet existe : `apt-cache search <package>`
2. Supprimez ou remplacez le paquet
3. Committez et re-déclenchez le build

### Build timeout après 45 minutes

**Problème :** `sudo timeout 2700 lb build` dépasse la limite.

**Solution :**
- Réduisez la liste des packages
- Utilisez des miroirs plus rapides
- Contactez l'administrateur pour augmenter la limite

### "live-image-amd64.hybrid.iso not found"

**Problème :** Le build n'a pas généré d'ISO.

**Causes possibles :**
- Espace disque insuffisant
- Erreur dans `nexos-launch.sh`
- Paquet invalide dans la liste

**Solution :**
1. Vérifiez les logs du step "Build ISO"
2. Cherchez les erreurs `dpkg` ou `lb`
3. Corrigez et re-déclenchez

## Fichiers de configuration

| Fichier | Description |
|---------|-------------|
| `.github/workflows/build-nexos-iso.yml` | Workflow GitHub Actions |
| `nexos-live/build.sh` | Script local de build |
| `nexos-live/nexos.list.chroot` | Liste des packages inclus |
| `nexos-live/config/hooks/normal/` | Hooks de build custom |

## Documentation supplémentaire

- [Debian Live Manual](https://live-team.pages.debian.net/live-manual/html/live-manual.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

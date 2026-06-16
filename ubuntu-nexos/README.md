# Nexos Ubuntu Overlay

Ce dossier contient un gestionnaire simple pour installer Nexos comme une couche réversible sur un système Ubuntu Xorg.

## Objectif

- Installer Nexos sans modifier l'interface Ubuntu d'origine.
- Laisser Ubuntu intact tant que Nexos est désinstallé.
- Fournir une commande pour installer, désactiver, réactiver et supprimer Nexos.

## Comment utiliser

1. Placez-vous dans le dossier `ubuntu-nexos` du dépôt :

```bash
cd /chemin/vers/nexos/ubuntu-nexos
```

2. Installez Nexos :

```bash
sudo ./nexos install
```

3. Lancez Nexos depuis le menu des applications ou :

```bash
sudo /usr/local/bin/nexos-launch
```

## Modes

- `sudo ./nexos install` : installe le launcher Nexos et copie l'UI dans `/opt/nexos`.
- `sudo ./nexos disable` : désactive Nexos sans supprimer les fichiers.
- `sudo ./nexos enable` : réactive Nexos après l'avoir désactivé.
- `sudo ./nexos uninstall` : supprime uniquement les fichiers Nexos créés.
- `sudo ./nexos status` : affiche l'état actuel.

## Comportement

- Nexos est installé sous `/opt/nexos`.
- Le lanceur est installé dans `/usr/local/bin/nexos-launch`.
- L'entrée d'application se trouve dans `/usr/share/applications/nexos.desktop`.
- L'autostart est activé via `/etc/xdg/autostart/nexos-autostart.desktop`.
- La commande `disable` coupe vraiment le démarrage automatique et cache l'entrée d'application.
- La commande `enable` rétablit l'autostart et l'entrée d'application.
- La commande `uninstall` supprime uniquement les fichiers Nexos, rien d'autre.

## Remarques

- Ce script ne modifie pas les fichiers utilisateur ou l'interface GNOME/Ubuntu existante.
- Fermer la fenêtre Nexos retourne à l'interface d'origine.
- Si `nexos-live/index.html` n'est pas présent, l'installation échouera avec un message clair.

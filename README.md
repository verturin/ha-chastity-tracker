# Chastity Tracker — Intégration Home Assistant

Intégration custom pour Home Assistant qui récupère automatiquement tes statistiques depuis l'extension phpBB **Chastity Tracker** de [cage-et-chastete.com](https://cage-et-chastete.com).

## Installation via HACS

1. HACS → menu ⋮ (en haut à droite) → **Dépôts personnalisés**
2. Coller l'URL de ce dépôt GitHub, catégorie **Intégration**
3. Rechercher "Chastity Tracker" dans HACS → **Télécharger**
4. Redémarrer Home Assistant
5. **Paramètres → Appareils et services → Ajouter une intégration** → chercher "Chastity Tracker"
6. Renseigner :
   - **URL du forum** (ex: `https://cage-et-chastete.com`)
   - **Token API** (généré dans UCP → Confidentialité → Accès API externe)

C'est tout — aucun YAML à écrire.

## Entités créées

| Entité | Description |
|---|---|
| `binary_sensor.cage` | Verrouillé / déverrouillé |
| `sensor.statut` | Statut texte |
| `sensor.jours_en_cours` | Jours de la période active |
| `sensor.jours_depuis_la_derniere_periode` | Jours écoulés depuis la fin |
| `sensor.total_cumule` | Total de jours cumulés |
| `sensor.jours_cette_annee` | Jours sur l'année en cours |
| `sensor.phrase_personnalisee` | Tagline (désactivée par défaut) |

## Mise à jour

Automatique via HACS dès qu'une nouvelle version est publiée sur le dépôt.

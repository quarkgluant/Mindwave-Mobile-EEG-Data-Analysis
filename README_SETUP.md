# Configuration MindWave Mobile EEG sur Linux Ubuntu

Ce répertoire contient les outils pour lire et enregistrer les données EEG du casque **NeuroSky MindWave Mobile** sur Ubuntu Linux.

## Prérequis

- Ubuntu 24.04 LTS (ou similaire)
- Python 3
- Bluetooth activé
- MindWave Mobile apparié (adresse MAC: `E0:7D:EA:E6:50:3C`)

## Installation

Les dépendances ont déjà été installées :
- `libbluetooth-dev` - Bibliothèques Bluetooth
- `python3-pip` - Gestionnaire de paquets Python
- `pyserial` - Communication série Python

## Structure des fichiers

```
Mindwave-Mobile-EEG-Data-Analysis/
├── python-mindwave/          # Bibliothèque Python pour MindWave
├── connect_mindwave.sh        # Script de connexion automatique
├── test_mindwave.py          # Script de test simple
├── record_eeg.py             # Script d'enregistrement CSV
├── data/                     # Dossier pour les enregistrements
└── README_SETUP.md           # Ce fichier
```

## Utilisation

### 1. Connexion du casque

Avant toute utilisation, assurez-vous que le casque est allumé et lancez :

```bash
./connect_mindwave.sh
```

Ce script :
- Crée le port série Bluetooth RFCOMM (`/dev/rfcomm0`)
- Configure les permissions appropriées
- Affiche les commandes disponibles

### 2. Test simple

Pour tester la connexion et voir les données en temps réel :

```bash
python3 test_mindwave.py
```

Affiche :
- Valeur brute EEG (raw value)
- Niveau d'attention (0-100)
- Niveau de méditation (0-100)
- Force du clignement
- Qualité du signal (0 = excellent, 255 = mauvais)

Appuyez sur `Ctrl+C` pour arrêter.

### 3. Enregistrement des données

Pour enregistrer les données dans un fichier CSV :

```bash
# Enregistrement continu (arrêt manuel avec Ctrl+C)
python3 record_eeg.py

# Enregistrement de 60 secondes
python3 record_eeg.py -d 60

# Enregistrement de 5 minutes (300 secondes)
python3 record_eeg.py -d 300
```

Les fichiers sont enregistrés dans `data/eeg_data_YYYYMMDD_HHMMSS.csv`

### Format des données CSV

Les fichiers CSV contiennent les colonnes suivantes :

| Colonne       | Description                           | Plage      |
|---------------|---------------------------------------|------------|
| timestamp     | Horodatage ISO 8601                   | -          |
| count         | Compteur de paquets                   | 0-99       |
| raw_value     | Valeur EEG brute (512 Hz)             | -32768 à 32767 |
| attention     | Niveau d'attention                    | 0-100      |
| meditation    | Niveau de méditation                  | 0-100      |
| blink         | Force du clignement                   | 0-255      |
| poor_signal   | Qualité du signal (0 = meilleur)      | 0-255      |

## Données EEG disponibles

### Valeurs calculées par le casque

- **Attention** : Indicateur de concentration/focus (eSense)
- **Meditation** : Indicateur de relaxation/calme (eSense)
- **Blink** : Détection et force des clignements d'yeux

### Valeur brute

- **Raw Value** : Signal EEG brut à 512 Hz, peut être utilisé pour :
  - Analyse des bandes de fréquences (delta, theta, alpha, beta, gamma)
  - Traitement du signal personnalisé
  - Algorithmes BCI (Brain-Computer Interface)

## Conseils d'utilisation

### Positionnement du casque

1. **Capteur frontal** : Placer sur le front, légèrement au-dessus du sourcil gauche
2. **Clip d'oreille** : Attacher fermement au lobe de l'oreille gauche
3. **Peau propre** : Nettoyer la zone de contact (pas de maquillage, huile, etc.)

### Qualité du signal

- **Signal < 5** : Excellent, données fiables
- **Signal 5-50** : Bon, utilisable
- **Signal > 50** : Mauvais, réajuster le casque

Le message "D-Bus experimental not enabled" peut être ignoré, il n'affecte pas le fonctionnement.

## Dépannage

### Le port `/dev/rfcomm0` n'existe pas

```bash
# Vérifier l'appairage Bluetooth
bluetoothctl devices

# Vérifier l'état du casque
bluetoothctl info E0:7D:EA:E6:50:3C

# Réexécuter le script de connexion
./connect_mindwave.sh
```

### Permission refusée

```bash
# Ajuster les permissions
sudo chmod 666 /dev/rfcomm0
```

### Le casque se déconnecte immédiatement

- Assurez-vous que le casque est en mode appairage (LED bleue clignotante)
- Relancez `./connect_mindwave.sh`
- Vérifiez que le casque n'est pas connecté à un autre appareil

### Signal toujours mauvais (> 50)

1. Nettoyez le capteur frontal avec un chiffon sec
2. Nettoyez votre peau (front et oreille)
3. Réajustez le casque
4. Humidifiez légèrement le clip d'oreille si nécessaire

## Ressources

- **Documentation NeuroSky** : http://neurosky.com/
- **ThinkGear Protocol** : Protocole série utilisé par le MindWave
- **Python-Mindwave** : https://github.com/faturita/python-mindwave

## Licence

- `python-mindwave` : Voir le dépôt original
- Scripts personnalisés : Usage libre pour ce projet

## Support

Pour toute question, consultez la documentation NeuroSky ou le README du projet python-mindwave.

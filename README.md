# MindWave Mobile EEG Data Analysis

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)](https://linux.org)

A comprehensive Python application for collecting, analyzing, and visualizing EEG data from the MindWave Mobile headset. This project provides both command-line tools and a graphical interface for real-time brainwave monitoring.

## Features

- **Bluetooth Connection Management**: Easy connection/disconnection to MindWave Mobile headset
- **Real-time EEG Monitoring**: Live visualization of brainwave data
- **Signal Quality Assessment**: Visual feedback for signal strength
- **Data Recording**: Save EEG sessions for later analysis
- **Graphical Interface**: User-friendly Tkinter-based GUI
- **Command Line Tools**: Script-based automation
- **Multi-language Support**: French and English documentation

## Quick Start

### Prerequisites

- Linux operating system
- Python 3.8+
- Bluetooth adapter
- MindWave Mobile headset
- sudo privileges for Bluetooth operations

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Mindwave-Mobile-EEG-Data-Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make scripts executable:
```bash
chmod +x connect_mindwave.sh disconnect_mindwave.sh
```

### Usage

#### Graphical Interface (Recommended)

Launch the GUI application:
```bash
python3 mindwave_gui.py
```

Or with sudo password pre-configured:
```bash
SUDO_PASSWORD="your_password" python3 mindwave_gui.py
```

#### Command Line

1. Connect the headset:
```bash
./connect_mindwave.sh
```

2. Test the connection:
```bash
python3 test_mindwave.py
```

3. Record EEG data:
```bash
python3 record_eeg.py -d 60  # 60 seconds recording
```

4. Disconnect:
```bash
./disconnect_mindwave.sh
```

## Project Structure

```
Mindwave-Mobile-EEG-Data-Analysis/
├── mindwave_gui.py              # Main GUI application
├── test_mindwave.py             # Command-line testing tool
├── record_eeg.py                # EEG recording utility
├── connect_mindwave.sh          # Bluetooth connection script
├── disconnect_mindwave.sh       # Bluetooth disconnection script
├── python-mindwave/             # MindWave driver library
├── data/                        # Recorded EEG data storage
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## GUI Features

The graphical interface provides:

- **Connection Management**: Connect/disconnect buttons with sudo handling
- **Signal Visualization**: Real-time vumeters for:
  - Signal strength (0-255)
  - Attention levels (0-100%)
  - Meditation levels (0-100%)
  - Blink detection (0-100%)
- **Recording Controls**: Duration selection and start/stop functionality
- **Activity Log**: Real-time status and error messages
- **Responsive Design**: Resizable window with proper layout

## EEG Data Metrics

The application monitors several key metrics:

- **Poor Signal**: Signal quality (255 = poor, 0 = excellent)
- **Attention**: Concentration level (0-100%)
- **Meditation**: Relaxation level (0-100%)
- **Blink Strength**: Eye blink detection (0-100%)
- **Raw EEG**: Unprocessed brainwave data

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure scripts are executable and sudo is available
2. **Bluetooth Connection**: Check if the headset is paired and in range
3. **Signal Quality**: Adjust headset position and ensure good contact
4. **Import Errors**: Verify all dependencies are installed

### Debug Mode

Enable verbose logging by setting the environment variable:
```bash
export DEBUG=1
python3 mindwave_gui.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **MindWave Mobile headset and SDK** - NeuroSky for the innovative EEG technology
- **Python community** for excellent libraries and tools
- **Bluetooth protocol contributors** for making wireless communication possible
- **faturita/python-mindwave** - Original Python driver for MindWave devices that inspired this project
- **NeuroSky ThinkGear Protocol** - The communication protocol that enables EEG data transmission

---

# MindWave Mobile EEG Data Analysis (Français)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)](https://linux.org)

Une application Python complète pour collecter, analyser et visualiser les données EEG du casque MindWave Mobile. Ce projet fournit à la fois des outils en ligne de commande et une interface graphique pour la surveillance des ondes cérébrales en temps réel.

## Fonctionnalités

- **Gestion de Connexion Bluetooth** : Connexion/déconnexion facile au casque MindWave Mobile
- **Surveillance EEG en Temps Réel** : Visualisation live des données d'ondes cérébrales
- **Évaluation de Qualité de Signal** : Feedback visuel pour la force du signal
- **Enregistrement de Données** : Sauvegarde des sessions EEG pour analyse ultérieure
- **Interface Graphique** : GUI conviviale basée sur Tkinter
- **Outils en Ligne de Commande** : Automatisation par scripts
- **Support Multilingue** : Documentation française et anglaise

## Démarrage Rapide

### Prérequis

- Système d'exploitation Linux
- Python 3.8+
- Adaptateur Bluetooth
- Casque MindWave Mobile
- Privilèges sudo pour les opérations Bluetooth

### Installation

1. Cloner le dépôt :
```bash
git clone <repository-url>
cd Mindwave-Mobile-EEG-Data-Analysis
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Rendre les scripts exécutables :
```bash
chmod +x connect_mindwave.sh disconnect_mindwave.sh
```

### Utilisation

#### Interface Graphique (Recommandé)

Lancer l'application GUI :
```bash
python3 mindwave_gui.py
```

Ou avec mot de passe sudo pré-configuré :
```bash
SUDO_PASSWORD="votre_mot_de_passe" python3 mindwave_gui.py
```

#### Ligne de Commande

1. Connecter le casque :
```bash
./connect_mindwave.sh
```

2. Tester la connexion :
```bash
python3 test_mindwave.py
```

3. Enregistrer les données EEG :
```bash
python3 record_eeg.py -d 60  # enregistrement de 60 secondes
```

4. Déconnecter :
```bash
./disconnect_mindwave.sh
```

## Structure du Projet

```
Mindwave-Mobile-EEG-Data-Analysis/
├── mindwave_gui.py              # Application GUI principale
├── test_mindwave.py             # Outil de test en ligne de commande
├── record_eeg.py                # Utilitaire d'enregistrement EEG
├── connect_mindwave.sh          # Script de connexion Bluetooth
├── disconnect_mindwave.sh       # Script de déconnexion Bluetooth
├── python-mindwave/             # Bibliothèque de pilote MindWave
├── data/                        # Stockage des données EEG enregistrées
├── requirements.txt              # Dépendances Python
└── README.md                    # Ce fichier
```

## Fonctionnalités GUI

L'interface graphique fournit :

- **Gestion de Connexion** : Boutons connecter/déconnecter avec gestion sudo
- **Visualisation de Signal** : Vumètres en temps réel pour :
  - Force du signal (0-255)
  - Niveaux d'attention (0-100%)
  - Niveaux de méditation (0-100%)
  - Détection de clignement (0-100%)
- **Contrôles d'Enregistrement** : Sélection de durée et démarrage/arrêt
- **Journal d'Activité** : Messages de statut et d'erreur en temps réel
- **Design Responsive** : Fenêtre redimensionnable avec mise en page appropriée

## Métriques des Données EEG

L'application surveille plusieurs métriques clés :

- **Poor Signal** : Qualité du signal (255 = mauvais, 0 = excellent)
- **Attention** : Niveau de concentration (0-100%)
- **Méditation** : Niveau de relaxation (0-100%)
- **Blink Strength** : Détection de clignement d'œil (0-100%)
- **Raw EEG** : Données d'ondes cérébrales non traitées

## Dépannage

### Problèmes Courants

1. **Permission Refusée** : Assurez-vous que les scripts sont exécutables et sudo disponible
2. **Connexion Bluetooth** : Vérifiez que le casque est appairé et à portée
3. **Qualité de Signal** : Ajustez la position du casque et assurez un bon contact
4. **Erreurs d'Import** : Vérifiez que toutes les dépendances sont installées

### Mode Débogage

Activez le logging verbeux en définissant la variable d'environnement :
```bash
export DEBUG=1
python3 mindwave_gui.py
```

## Contribution

1. Forker le dépôt
2. Créer une branche de fonctionnalité
3. Apporter vos modifications
4. Ajouter des tests si applicable
5. Soumettre une pull request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

## Remerciements

- **MindWave Mobile et SDK** - NeuroSky pour la technologie EEG innovante
- **Communauté Python** pour ses excellentes bibliothèques et outils
- **Contributeurs du protocole Bluetooth** pour rendre la communication sans fil possible
- **faturita/python-mindwave** - Pilote Python original pour les appareils MindWave qui a inspiré ce projet
- **NeuroSky ThinkGear Protocol** - Le protocole de communication qui permet la transmission des données EEG

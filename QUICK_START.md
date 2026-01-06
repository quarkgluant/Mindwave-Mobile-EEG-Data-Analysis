# Guide de démarrage rapide - MindWave Mobile

## 🚀 Utilisation en 3 étapes

### Étape 1 : Préparer le casque
1. Allumer le MindWave Mobile (bouton sur le côté)
2. La LED doit clignoter en bleu (mode appairage) ou être fixe (connecté)
3. Porter le casque :
   - Capteur sur le front (au-dessus du sourcil gauche)
   - Clip sur le lobe de l'oreille gauche

### Étape 2 : Connecter
```bash
cd ~/Mindwave-Mobile-EEG-Data-Analysis
./connect_mindwave.sh
```

### Étape 3 : Utiliser

#### Option A : Test rapide
```bash
python3 test_mindwave.py
```
Affiche les données en temps réel. Appuyez sur `Ctrl+C` pour arrêter.

#### Option B : Enregistrement
```bash
# Enregistrement continu
python3 record_eeg.py

# Enregistrement de 2 minutes
python3 record_eeg.py -d 120
```

Les données sont sauvegardées dans `data/eeg_data_YYYYMMDD_HHMMSS.csv`

## 📊 Que signifient les données ?

- **Attention (0-100)** : Niveau de concentration
  - 0-40 : Faible
  - 40-60 : Neutre
  - 60-100 : Élevé

- **Meditation (0-100)** : Niveau de relaxation
  - 0-40 : Faible
  - 40-60 : Neutre
  - 60-100 : Élevé

- **Signal (0-255)** : Qualité de la connexion
  - 0-5 : Excellent ✅
  - 5-50 : Bon ⚠️
  - >50 : Mauvais ❌ (réajuster le casque)

- **Raw Value** : Signal EEG brut (512 échantillons/seconde)

## 🔧 Problèmes courants

### Le signal est mauvais (>50)
- Nettoyez le capteur frontal
- Nettoyez votre peau (front et oreille)
- Humidifiez légèrement le clip d'oreille
- Réajustez le casque

### Erreur "Permission denied"
```bash
sudo chmod 666 /dev/rfcomm0
```

### Le casque ne se connecte pas
```bash
# Vérifier l'appairage
bluetoothctl devices

# Reconnecter
./connect_mindwave.sh
```

## 📁 Analyser les données

Les fichiers CSV peuvent être ouverts avec :
- Excel / LibreOffice Calc
- Python (pandas, matplotlib)
- MATLAB / Octave
- R

Exemple Python :
```python
import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv('data/eeg_data_20260104_180000.csv')

# Tracer l'attention et la méditation
df[['attention', 'meditation']].plot()
plt.show()
```

## 💡 Conseils

1. **Environnement calme** : Réduisez les distractions pour de meilleurs résultats
2. **Position stable** : Ne bougez pas trop pendant l'enregistrement
3. **Durée** : Attendez 1-2 minutes pour que le casque se stabilise
4. **Calibration** : Les premières secondes peuvent être instables

## 📚 Documentation complète

Voir `README_SETUP.md` pour plus de détails sur :
- Format des données
- API Python
- Traitement du signal
- Résolution de problèmes

---

**Amusez-vous avec votre exploration des ondes cérébrales ! 🧠✨**

#!/usr/bin/env python3
"""
Enregistrement des données EEG du MindWave Mobile dans un fichier CSV
"""

import sys
import time
import csv
from datetime import datetime
sys.path.insert(0, '/home/quark/Mindwave-Mobile-EEG-Data-Analysis/python-mindwave')
import mindwave

# Configuration
DEVICE_PATH = '/dev/rfcomm0'
DEVICE_MAC = 'E0:7D:EA:E6:50:3C'
OUTPUT_DIR = '/home/quark/Mindwave-Mobile-EEG-Data-Analysis/data'

class EEGRecorder:
    def __init__(self, device_path, output_dir):
        self.device_path = device_path
        self.output_dir = output_dir
        self.headset = None
        self.csv_file = None
        self.csv_writer = None
        self.data_count = 0
        
    def setup(self):
        """Initialiser la connexion et le fichier de sortie"""
        import os
        
        # Créer le répertoire de sortie si nécessaire
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Créer le nom du fichier avec timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.output_dir}/eeg_data_{timestamp}.csv"
        
        # Ouvrir le fichier CSV
        self.csv_file = open(filename, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Écrire l'en-tête
        self.csv_writer.writerow([
            'timestamp', 'count', 'raw_value', 
            'attention', 'meditation', 'blink', 'poor_signal'
        ])
        
        print(f"📝 Enregistrement dans: {filename}")
        
        # Initialiser le casque
        print("Connexion au casque...")
        self.headset = mindwave.Headset(self.device_path)
        
        # Attendre un bon signal
        print("Vérification de la qualité du signal...")
        wait_count = 0
        while self.headset.poor_signal > 5 and wait_count < 30:
            print(f"Signal: {self.headset.poor_signal}/255", end='\r')
            time.sleep(0.5)
            wait_count += 1
        
        if self.headset.poor_signal > 5:
            print(f"\n⚠️  Signal faible ({self.headset.poor_signal}/255), mais enregistrement démarré")
        else:
            print(f"\n✓ Signal OK ({self.headset.poor_signal}/255)")
        
        # Attacher le handler
        self.headset.raw_value_handlers.append(self.on_raw)
        
    def on_raw(self, headset, rawvalue):
        """Handler appelé pour chaque nouvelle valeur EEG"""
        timestamp = datetime.now().isoformat()
        
        # Écrire dans le CSV
        self.csv_writer.writerow([
            timestamp,
            headset.count,
            headset.raw_value,
            headset.attention,
            headset.meditation,
            headset.blink,
            headset.poor_signal
        ])
        
        self.data_count += 1
        
        # Afficher un message tous les 100 enregistrements
        if self.data_count % 100 == 0:
            print(f"📊 {self.data_count} échantillons enregistrés "
                  f"(A:{headset.attention}, M:{headset.meditation}, S:{headset.poor_signal})")
    
    def run(self, duration_seconds=None):
        """Lancer l'enregistrement"""
        print(f"\n🎙️  Enregistrement en cours...")
        if duration_seconds:
            print(f"Durée: {duration_seconds} secondes")
        print("(Ctrl+C pour arrêter)\n")
        
        start_time = time.time()
        try:
            while True:
                time.sleep(0.1)
                
                # Arrêter après la durée spécifiée
                if duration_seconds and (time.time() - start_time) > duration_seconds:
                    print(f"\n✓ Durée d'enregistrement atteinte")
                    break
        
        except KeyboardInterrupt:
            print("\n\n⏸️  Arrêt demandé par l'utilisateur")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Nettoyer les ressources"""
        print("\n📊 Statistiques finales:")
        print(f"  - Total d'échantillons: {self.data_count}")
        
        if self.headset:
            print("Fermeture de la connexion au casque...")
            self.headset.stop()
        
        if self.csv_file:
            self.csv_file.close()
            print("✓ Fichier CSV fermé")
        
        print("✓ Enregistrement terminé")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Enregistrer les données EEG du MindWave Mobile'
    )
    parser.add_argument(
        '-d', '--duration',
        type=int,
        default=None,
        help='Durée d\'enregistrement en secondes (par défaut: infini)'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Enregistreur de données EEG - MindWave Mobile")
    print("=" * 70)
    print(f"\nDevice: {DEVICE_PATH}")
    print(f"MAC Address: {DEVICE_MAC}\n")
    
    recorder = EEGRecorder(DEVICE_PATH, OUTPUT_DIR)
    recorder.setup()
    recorder.run(args.duration)

if __name__ == "__main__":
    main()

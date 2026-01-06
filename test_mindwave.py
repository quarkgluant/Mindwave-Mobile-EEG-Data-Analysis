#!/usr/bin/env python3
"""
Script de test pour le casque MindWave Mobile sur Linux
Lit et affiche les données EEG en temps réel
"""

import sys
import time
sys.path.insert(0, '/home/quark/Mindwave-Mobile-EEG-Data-Analysis/python-mindwave')
import mindwave

# Configuration
DEVICE_PATH = '/dev/rfcomm0'  # Port série Bluetooth RFCOMM
DEVICE_MAC = 'E0:7D:EA:E6:50:3C'  # Adresse MAC du MindWave Mobile

def on_raw(headset, rawvalue):
    """Handler pour les valeurs brutes EEG"""
    print(f"[{headset.count:3d}] Raw: {headset.raw_value:5d}, "
          f"Attention: {headset.attention:3d}, "
          f"Meditation: {headset.meditation:3d}, "
          f"Blink: {headset.blink:3d}, "
          f"Signal: {headset.poor_signal:3d}")

def main():
    print("=" * 70)
    print("Test du casque MindWave Mobile EEG")
    print("=" * 70)
    print(f"\nDevice: {DEVICE_PATH}")
    print(f"MAC Address: {DEVICE_MAC}")
    
    # Créer l'objet Headset
    # Pour MindWave Mobile via Bluetooth, pas besoin de headset_id
    print(f"\nInitialisation de la connexion au casque...")
    headset = mindwave.Headset(DEVICE_PATH)
    
    # Attendre que le signal soit bon
    print("\nVérification de la qualité du signal...")
    print("(Ajustez le casque et le clip d'oreille si nécessaire)")
    
    wait_count = 0
    while headset.poor_signal > 5 and wait_count < 30:
        print(f"Signal faible: {headset.poor_signal}/255. En attente...", end='\r')
        time.sleep(0.5)
        wait_count += 1
    
    if headset.poor_signal > 5:
        print("\n\n⚠️  ATTENTION: Le signal est toujours faible!")
        print("Assurez-vous que:")
        print("  - Le capteur est bien positionné sur le front")
        print("  - Le clip d'oreille est bien attaché au lobe")
        print("  - La peau est propre et sèche")
        print("\nContinuation malgré le signal faible...\n")
    else:
        print(f"\n✓ Signal OK: {headset.poor_signal}/255\n")
    
    # Attacher le handler pour les valeurs brutes
    headset.raw_value_handlers.append(on_raw)
    
    print("Lecture des données EEG en cours...")
    print("(Ctrl+C pour arrêter)\n")
    
    try:
        # Boucle principale
        while True:
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\nArrêt demandé par l'utilisateur...")
    
    finally:
        print("Fermeture de la connexion...")
        headset.stop()
        print("✓ Terminé")

if __name__ == "__main__":
    main()

#!/bin/bash
# Script pour connecter le MindWave Mobile via Bluetooth RFCOMM

DEVICE_MAC="E0:7D:EA:E6:50:3C"
RFCOMM_PORT="/dev/rfcomm0"
RFCOMM_CHANNEL=1

echo "==========================================="
echo "Connexion MindWave Mobile EEG"
echo "==========================================="
echo ""
echo "Device MAC: $DEVICE_MAC"
echo "RFCOMM Port: $RFCOMM_PORT"
echo ""

# Vérifier si rfcomm0 existe déjà
if [ -e "$RFCOMM_PORT" ]; then
    echo "⚠️  $RFCOMM_PORT existe déjà"
    echo "Libération du port..."
    sudo rfcomm release 0
    sleep 1
fi

# Créer la connexion RFCOMM
echo "Création de la connexion RFCOMM..."
sudo rfcomm bind 0 "$DEVICE_MAC" "$RFCOMM_CHANNEL"

# Vérifier que ça a fonctionné
if [ -e "$RFCOMM_PORT" ]; then
    echo "✓ Connexion établie: $RFCOMM_PORT"
    
    # Changer les permissions pour permettre l'accès utilisateur
    sudo chmod 666 "$RFCOMM_PORT"
    echo "✓ Permissions ajustées"
    
    echo ""
    echo "Le casque est prêt à l'emploi!"
    echo ""
    echo "Commandes disponibles:"
    echo "  - Test simple:        python3 test_mindwave.py"
    echo "  - Enregistrement:     python3 record_eeg.py"
    echo "  - Avec durée (60s):   python3 record_eeg.py -d 60"
    echo ""
else
    echo "❌ Erreur: Impossible de créer $RFCOMM_PORT"
    echo ""
    echo "Vérifiez que:"
    echo "  - Le casque est allumé"
    echo "  - Le casque est bien apparié en Bluetooth"
    echo "  - Vous avez les droits sudo"
    exit 1
fi

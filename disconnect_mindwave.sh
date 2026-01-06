#!/bin/bash
# Script pour déconnecter le MindWave Mobile et libérer le port RFCOMM

RFCOMM_PORT="/dev/rfcomm0"

echo "==========================================="
echo "Déconnexion MindWave Mobile EEG"
echo "==========================================="
echo ""

# Vérifier si le port existe
if [ -e "$RFCOMM_PORT" ]; then
    echo "Libération du port $RFCOMM_PORT..."
    sudo rfcomm release 0
    
    # Vérifier que c'est bien libéré
    if [ ! -e "$RFCOMM_PORT" ]; then
        echo "✓ Port libéré avec succès"
    else
        echo "⚠️  Le port existe encore, tentative forcée..."
        sudo rfcomm release 0 2>/dev/null
    fi
else
    echo "✓ Le port $RFCOMM_PORT n'existe pas (déjà libéré)"
fi

echo ""
echo "✓ Déconnexion terminée"
echo ""
echo "Pour reconnecter, utilisez: ./connect_mindwave.sh"

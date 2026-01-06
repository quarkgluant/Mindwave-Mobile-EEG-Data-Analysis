#!/usr/bin/env python3
"""
Interface graphique pour le casque MindWave Mobile EEG
Utilise Tkinter pour une interface légère et simple
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import subprocess
import threading
import time
import sys
import os
from pathlib import Path

# Ajout du chemin du module mindwave
sys.path.insert(0, str(Path(__file__).parent / 'python-mindwave'))
import mindwave

class MindwaveGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MindWave Mobile EEG - Interface Graphique")
        self.root.geometry("550x700")
        self.root.resizable(True, True)

        # Variables d'état
        self.is_connected = False
        self.is_recording = False
        self.is_testing = False
        self.headset = None
        self.test_thread = None
        self.record_thread = None
        self.sudo_password = "3.14159"

        # Variables pour le vumètre
        self.signal_strength = tk.IntVar(value=255)
        self.attention = tk.IntVar(value=0)
        self.meditation = tk.IntVar(value=0)
        self.blink = tk.IntVar(value=0)

        self.setup_ui()
        self.update_status()

    def setup_ui(self):
        """Configure l'interface graphique"""

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Section Connexion
        conn_frame = ttk.LabelFrame(main_frame, text="Connexion Bluetooth", padding="10")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.connect_btn = ttk.Button(conn_frame, text="Connecter", command=self.connect_device)
        self.connect_btn.grid(row=0, column=0, padx=5, pady=5)

        self.disconnect_btn = ttk.Button(conn_frame, text="Déconnecter", command=self.disconnect_device)
        self.disconnect_btn.grid(row=0, column=1, padx=5, pady=5)

        self.status_label = ttk.Label(conn_frame, text="État: Déconnecté", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=2, padx=20, pady=5)

        # Section Vumètre
        vumeter_frame = ttk.LabelFrame(main_frame, text="Signal EEG", padding="10")
        vumeter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Signal strength
        ttk.Label(vumeter_frame, text="Force du signal:").grid(row=0, column=0, sticky=tk.W)
        self.signal_bar = ttk.Progressbar(vumeter_frame, length=300, mode='determinate', maximum=255)
        self.signal_bar.grid(row=0, column=1, padx=10, pady=2)
        self.signal_value_label = ttk.Label(vumeter_frame, text="255/255")
        self.signal_value_label.grid(row=0, column=2, padx=5)

        # Attention
        ttk.Label(vumeter_frame, text="Attention:").grid(row=1, column=0, sticky=tk.W)
        self.attention_bar = ttk.Progressbar(vumeter_frame, length=300, mode='determinate', maximum=100)
        self.attention_bar.grid(row=1, column=1, padx=10, pady=2)
        self.attention_value_label = ttk.Label(vumeter_frame, text="0%")
        self.attention_value_label.grid(row=1, column=2, padx=5)

        # Meditation
        ttk.Label(vumeter_frame, text="Méditation:").grid(row=2, column=0, sticky=tk.W)
        self.meditation_bar = ttk.Progressbar(vumeter_frame, length=300, mode='determinate', maximum=100)
        self.meditation_bar.grid(row=2, column=1, padx=10, pady=2)
        self.meditation_value_label = ttk.Label(vumeter_frame, text="0%")
        self.meditation_value_label.grid(row=2, column=2, padx=5)

        # Blink
        ttk.Label(vumeter_frame, text="Clignement:").grid(row=3, column=0, sticky=tk.W)
        self.blink_bar = ttk.Progressbar(vumeter_frame, length=300, mode='determinate', maximum=100)
        self.blink_bar.grid(row=3, column=1, padx=10, pady=2)
        self.blink_value_label = ttk.Label(vumeter_frame, text="0%")
        self.blink_value_label.grid(row=3, column=2, padx=5)

        # Section Actions
        action_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.test_btn = ttk.Button(action_frame, text="Tester le casque", command=self.test_headset)
        self.test_btn.grid(row=0, column=0, padx=5, pady=5)

        # Section Enregistrement
        record_frame = ttk.LabelFrame(main_frame, text="Enregistrement EEG", padding="10")
        record_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(record_frame, text="Durée (secondes):").grid(row=0, column=0, sticky=tk.W)
        self.duration_var = tk.StringVar(value="60")
        duration_spinbox = ttk.Spinbox(record_frame, from_=10, to=300, textvariable=self.duration_var, width=10)
        duration_spinbox.grid(row=0, column=1, padx=5, pady=5)

        self.record_btn = ttk.Button(record_frame, text="Commencer l'enregistrement", command=self.start_recording)
        self.record_btn.grid(row=0, column=2, padx=5, pady=5)

        self.stop_record_btn = ttk.Button(record_frame, text="Arrêter", command=self.stop_recording, state=tk.DISABLED)
        self.stop_record_btn.grid(row=0, column=3, padx=5, pady=5)

        # Section Log
        log_frame = ttk.LabelFrame(main_frame, text="Journal", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(4, weight=1)  # Permet l'expansion du log

        self.log_text = tk.Text(log_frame, height=12, width=70, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        # Bouton pour effacer le log
        clear_btn = ttk.Button(log_frame, text="Effacer", command=self.clear_log)
        clear_btn.grid(row=1, column=0, pady=5)

        self.log("Interface MindWave Mobile EEG prête")

    def get_sudo_password(self):
        """Demande le mot de passe sudo à l'utilisateur"""
        if self.sudo_password is None:
            password = simpledialog.askstring("Mot de passe requis",
                                             "Entrez votre mot de passe sudo:",
                                             show='*',
                                             parent=self.root)
            if password:
                self.sudo_password = password
                return password
            else:
                return None
        return self.sudo_password

    def log(self, message):
        """Ajoute un message au journal"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        """Efface le journal"""
        self.log_text.delete(1.0, tk.END)

    def connect_device(self):
        """Connecte le casque via le script shell"""
        if self.is_connected:
            messagebox.showwarning("Attention", "Le casque est déjà connecté")
            return

        self.log("Connexion du casque...")
        self.connect_btn.config(state=tk.DISABLED)

        def connect_thread():
            try:
                # Obtenir le mot de passe sudo
                password = self.get_sudo_password()
                if not password:
                    self.log("✗ Mot de passe non fourni - connexion annulée")
                    return

                # Exécuter avec sudo en utilisant le mot de passe
                env = os.environ.copy()
                process = subprocess.Popen(['sudo', '-S', './connect_mindwave.sh'],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        env=env)

                stdout, stderr = process.communicate(input=password + '\n', timeout=30)

                if process.returncode == 0:
                    self.is_connected = True
                    self.log("✓ Casque connecté avec succès")
                    self.root.after(0, self.update_connection_ui)
                else:
                    self.log(f"✗ Erreur de connexion: {stderr}")
                    messagebox.showerror("Erreur", f"Échec de la connexion: {stderr}")
                    # Réinitialiser le mot de passe en cas d'erreur
                    self.sudo_password = None

            except subprocess.TimeoutExpired:
                self.log("✗ Timeout lors de la connexion")
                messagebox.showerror("Erreur", "Timeout lors de la connexion")
                self.sudo_password = None
            except Exception as e:
                self.log(f"✗ Erreur: {str(e)}")
                messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")
                self.sudo_password = None
            finally:
                self.root.after(0, lambda: self.connect_btn.config(state=tk.NORMAL))

        threading.Thread(target=connect_thread, daemon=True).start()

    def disconnect_device(self):
        """Déconnecte le casque via le script shell"""
        if not self.is_connected:
            messagebox.showwarning("Attention", "Le casque n'est pas connecté")
            return

        self.log("Déconnexion du casque...")
        self.disconnect_btn.config(state=tk.DISABLED)

        # Arrêter les processus en cours
        if self.is_testing:
            self.stop_testing()
        if self.is_recording:
            self.stop_recording()

        def disconnect_thread():
            try:
                # Obtenir le mot de passe sudo
                password = self.get_sudo_password()
                if not password:
                    self.log("✗ Mot de passe non fourni - déconnexion annulée")
                    return

                # Exécuter avec sudo en utilisant le mot de passe
                env = os.environ.copy()
                process = subprocess.Popen(['sudo', '-S', './disconnect_mindwave.sh'],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        env=env)

                stdout, stderr = process.communicate(input=password + '\n', timeout=15)

                if process.returncode == 0:
                    self.is_connected = False
                    self.log("✓ Casque déconnecté")
                    self.root.after(0, self.update_connection_ui)
                else:
                    self.log(f"✗ Erreur de déconnexion: {stderr}")
                    messagebox.showerror("Erreur", f"Échec de la déconnexion: {stderr}")
                    # Réinitialiser le mot de passe en cas d'erreur
                    self.sudo_password = None

            except subprocess.TimeoutExpired:
                self.log("✗ Timeout lors de la déconnexion")
                messagebox.showerror("Erreur", "Timeout lors de la déconnexion")
                self.sudo_password = None
            except Exception as e:
                self.log(f"✗ Erreur: {str(e)}")
                messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")
                self.sudo_password = None
            finally:
                self.root.after(0, lambda: self.disconnect_btn.config(state=tk.NORMAL))

        threading.Thread(target=disconnect_thread, daemon=True).start()

    def update_connection_ui(self):
        """Met à jour l'interface selon l'état de connexion"""
        if self.is_connected:
            self.status_label.config(text="État: Connecté", foreground="green")
            self.test_btn.config(state=tk.NORMAL)
            self.record_btn.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="État: Déconnecté", foreground="red")
            self.test_btn.config(state=tk.DISABLED)
            self.record_btn.config(state=tk.DISABLED)
            # Réinitialiser les vumètres
            self.signal_strength.set(255)
            self.attention.set(0)
            self.meditation.set(0)
            self.blink.set(0)
            self.update_vumeters()

    def test_headset(self):
        """Lance le test du casque"""
        if not self.is_connected:
            messagebox.showwarning("Attention", "Veuillez d'abord connecter le casque")
            return

        if self.is_testing:
            messagebox.showwarning("Attention", "Test déjà en cours")
            return

        self.log("Démarrage du test du casque...")
        self.test_btn.config(state=tk.DISABLED)
        self.is_testing = True

        def test_thread():
            try:
                # Initialiser le casque
                self.headset = mindwave.Headset('/dev/rfcomm0')

                # Handler pour mettre à jour les vumètres
                def update_handler(headset, value):
                    self.root.after(0, lambda: self.update_signal_values(headset))

                self.headset.raw_value_handlers.append(update_handler)

                # Attendre que le signal soit bon
                wait_count = 0
                while self.headset.poor_signal > 5 and wait_count < 30 and self.is_testing:
                    self.root.after(0, lambda: self.update_signal_values(self.headset))
                    time.sleep(0.5)
                    wait_count += 1

                if self.is_testing:
                    self.log("✓ Test démarré - Surveillance des données EEG")

                    # Boucle de surveillance
                    while self.is_testing:
                        self.root.after(0, lambda: self.update_signal_values(self.headset))
                        time.sleep(0.1)

            except Exception as e:
                self.log(f"✗ Erreur lors du test: {str(e)}")
                messagebox.showerror("Erreur", f"Erreur lors du test: {str(e)}")
            finally:
                if self.headset:
                    self.headset.stop()
                    self.headset = None
                self.is_testing = False
                self.root.after(0, lambda: self.test_btn.config(state=tk.NORMAL))
                self.log("Test terminé")

        self.test_thread = threading.Thread(target=test_thread, daemon=True)
        self.test_thread.start()

    def stop_testing(self):
        """Arrête le test en cours"""
        self.is_testing = False
        self.log("Arrêt du test...")

    def update_signal_values(self, headset):
        """Met à jour les valeurs des vumètres"""
        if headset:
            self.signal_strength.set(headset.poor_signal)
            self.attention.set(headset.attention)
            self.meditation.set(headset.meditation)
            self.blink.set(headset.blink)
            self.update_vumeters()

    def update_vumeters(self):
        """Met à jour l'affichage des vumètres"""
        # Signal (inversé: 255 = mauvais, 0 = bon)
        signal_val = self.signal_strength.get()
        self.signal_bar['value'] = 255 - signal_val
        self.signal_value_label.config(text=f"{signal_val}/255")

        # Attention et Meditation (0-100)
        att_val = self.attention.get()
        med_val = self.meditation.get()
        self.attention_bar['value'] = att_val
        self.attention_value_label.config(text=f"{att_val}%")
        self.meditation_bar['value'] = med_val
        self.meditation_value_label.config(text=f"{med_val}%")

        # Blink (0-100)
        blink_val = self.blink.get()
        self.blink_bar['value'] = blink_val
        self.blink_value_label.config(text=f"{blink_val}%")

    def start_recording(self):
        """Commence l'enregistrement EEG"""
        if not self.is_connected:
            messagebox.showwarning("Attention", "Veuillez d'abord connecter le casque")
            return

        if self.is_recording:
            messagebox.showwarning("Attention", "Enregistrement déjà en cours")
            return

        try:
            duration = int(self.duration_var.get())
            if duration < 10 or duration > 300:
                messagebox.showerror("Erreur", "La durée doit être entre 10 et 300 secondes")
                return
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer une durée valide")
            return

        self.log(f"Démarrage de l'enregistrement pour {duration} secondes...")
        self.record_btn.config(state=tk.DISABLED)
        self.stop_record_btn.config(state=tk.NORMAL)
        self.is_recording = True

        def record_thread():
            try:
                cmd = ['python3', 'record_eeg.py', '-d', str(duration)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration+30)

                if result.returncode == 0:
                    self.log(f"✓ Enregistrement terminé ({duration}s)")
                    messagebox.showinfo("Succès", f"Enregistrement terminé avec succès")
                else:
                    self.log(f"✗ Erreur d'enregistrement: {result.stderr}")
                    messagebox.showerror("Erreur", f"Échec de l'enregistrement: {result.stderr}")

            except subprocess.TimeoutExpired:
                self.log("✗ Timeout lors de l'enregistrement")
                messagebox.showerror("Erreur", "Timeout lors de l'enregistrement")
            except Exception as e:
                self.log(f"✗ Erreur: {str(e)}")
                messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")
            finally:
                self.is_recording = False
                self.root.after(0, self.update_recording_ui)

        self.record_thread = threading.Thread(target=record_thread, daemon=True)
        self.record_thread.start()

    def stop_recording(self):
        """Arrête l'enregistrement en cours"""
        self.is_recording = False
        self.log("Arrêt de l'enregistrement...")
        # Note: L'arrêt propre dépend de l'implémentation de record_eeg.py

    def update_recording_ui(self):
        """Met à jour l'interface d'enregistrement"""
        self.record_btn.config(state=tk.NORMAL)
        self.stop_record_btn.config(state=tk.DISABLED)

    def update_status(self):
        """Met à jour périodiquement l'affichage"""
        if self.is_testing and self.headset:
            self.update_signal_values(self.headset)
        self.root.after(100, self.update_status)

    def run(self):
        """Démarre l'interface graphique"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MindwaveGUI()
    app.run()

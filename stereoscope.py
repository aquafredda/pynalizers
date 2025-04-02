import numpy as np
import librosa
import matplotlib.pyplot as plt
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate stereoscope visualization from audio file.')
    parser.add_argument('audio_file', help='Path to the stereo audio file')
    parser.add_argument('start_time', type=float, help='Start time in seconds')
    parser.add_argument('duration', type=float, help='Duration in seconds')
    parser.add_argument('output_png', help='Output PNG file path')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for output image (default: 300)')
    parser.add_argument('--markersize', type=float, default=0.5, help='Size of plot markers (default: 0.5)')
    parser.add_argument('--alpha', type=float, default=0.5, help='Alpha transparency of markers (default: 0.5)')
    return parser.parse_args()

# Parse arguments
args = parse_arguments()

# Caricamento audio
try:
    y, sr = librosa.load(args.audio_file, sr=None, mono=False, offset=args.start_time, duration=args.duration)
except FileNotFoundError:
    print(f"Errore: Il file audio '{args.audio_file}' non è stato trovato.")
    sys.exit(1)
except Exception as e:
    print(f"Errore durante il caricamento dell'audio: {e}")
    sys.exit(1)

# Controllo canali
if y.ndim == 1:
    print("Audio mono rilevato. Convertire in stereo per lo stereoscope.")
    sys.exit(1)

# Estrazione canali
left, right = y[0], y[1]

# Calcolo Mid/Side corretto
Mid = (left + right) / 2  # Mid (mono)
Side = (right - left) / 2  # Side (differenza). Negli stereoscopi la visualizzazione è invertita

# Per il grafico, usiamo il formato standard
X = Side  # Asse X rappresenta Side
Y = Mid   # Asse Y rappresenta Mid

# Calcolo percentuali energia
mid_energy = np.sum(Mid**2)
side_energy = np.sum(Side**2)
total_energy = mid_energy + side_energy
mid_percentage = (mid_energy / total_energy) * 100 if total_energy > 0 else 0

# Creazione finestra con due subplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 5),
                              gridspec_kw={'width_ratios': [3, 0.3]})

# Grafico principale
ax1.plot(X, Y, '.', markersize=args.markersize, alpha=args.alpha, color='black')
ax1.axhline(0, color='gray', linewidth=0.5)
ax1.axvline(0, color='gray', linewidth=0.5)
ax1.set_aspect('equal')  # Imposta aspetto quadrato
ax1.grid(True, linestyle='--', linewidth=0.5)

# Imposta gli stessi limiti per assi X e Y per mantenere proporzioni
max_range = max(np.max(np.abs(X)), np.max(np.abs(Y)))
ax1.set_xlim(-max_range, max_range)
ax1.set_ylim(-max_range, max_range)

# Barra verticale in bianco e nero per rappresentare la percentuale di Mid
ax2.set_ylim(0, 100)
ax2.set_xlim(0, 1)

# Barra nera per Mid, il resto bianco
ax2.bar(0.5, 100, width=1, color='white', edgecolor='black')  # Sfondo bianco
ax2.bar(0.5, mid_percentage, width=1, color='black', edgecolor='black')  # Barra nera per Mid

# Etichetta percentuale in basso alla barra, dritta
ax2.text(0.5, -2, f"Mid: {mid_percentage:.1f}%", ha='center', va='top', color='black', fontweight='bold')

# Rimuovi etichette inutili
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_ylabel("")
ax2.set_xlabel("")
ax2.axis('Off')

plt.tight_layout()
try:
    plt.savefig(args.output_png, dpi=args.dpi)
    print(f"Immagine salvata con successo: {args.output_png}")
except Exception as e:
    print(f"Errore durante il salvataggio dell'immagine: {e}")
    sys.exit(1)

plt.show()

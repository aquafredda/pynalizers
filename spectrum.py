import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse
from scipy import signal as sg
from scipy.ndimage import gaussian_filter1d
import os
import warnings

def analyze_audio_file(input_file, fs_out=None, signal_out=None, analysis_second=7, window_size=10):
    """
    Analizza un file audio e restituisce la frequenza di campionamento e il segnale elaborato.
    Se fs_out e signal_out sono forniti, li restituisce insieme ai nuovi valori.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=wavfile.WavFileWarning)
        fs, original_signal = wavfile.read(input_file)

    if len(original_signal.shape) > 1:
        original_signal = np.mean(original_signal, axis=1)

    # Normalizzazione del segnale
    if original_signal.dtype == np.int16:
        signal = original_signal / 32768.0
    elif original_signal.dtype == np.int32:
        signal = original_signal / 2147483648.0
    elif original_signal.dtype == np.float32 or original_signal.dtype == np.float64:
        signal = original_signal
    else:
        signal = original_signal / np.iinfo(original_signal.dtype).max

    # Ricampionamento a 48kHz se necessario
    target_fs = 48000
    if fs != target_fs:
        num_samples = int(len(signal) * target_fs / fs)
        signal = sg.resample(signal, num_samples)
        fs = target_fs

    # Seleziona il segmento da analizzare
    duration = len(signal) / fs
    if analysis_second >= duration:
        analysis_second = duration - window_size

    start_sample = int(analysis_second * fs)
    window_samples = int(window_size * fs)
    segment = signal[start_sample:start_sample + window_samples]

    # Applica finestra di Hann
    window = sg.windows.hann(len(segment))
    segment_windowed = segment * window

    # Calcola la FFT
    n_fft = max(16384, window_samples)
    fft_result = np.fft.rfft(segment_windowed, n=n_fft)
    freq = np.fft.rfftfreq(n_fft, d=1/fs)
    magnitude = np.abs(fft_result) / (n_fft/2)
    magnitude[1:-1] = magnitude[1:-1] * 2
    dbfs = 20 * np.log10(np.clip(magnitude, 1e-10, None))
    dbfs = gaussian_filter1d(dbfs, sigma=100)

    if fs_out is not None and signal_out is not None:
        return fs, freq, dbfs, fs_out, signal_out
    else:
        return fs, freq, dbfs

def compare_audio_files(input_file1, input_file2, output_file, analysis_second=7, window_size=10, label1=None, label2=None):
    """
    Confronta due file audio generando un grafico che sovrappone i loro spettri.
    """
    # Analizza i due file audio
    fs1, freq1, dbfs1 = analyze_audio_file(input_file1, analysis_second=analysis_second, window_size=window_size)
    fs2, freq2, dbfs2 = analyze_audio_file(input_file2, analysis_second=analysis_second, window_size=window_size)

    # Se non sono fornite etichette, usa i nomi dei file
    if label1 is None:
        label1 = os.path.basename(input_file1)
    if label2 is None:
        label2 = os.path.basename(input_file2)

    # Crea il grafico
    plt.figure(figsize=(12, 4))
    plt.semilogx(freq1, dbfs1, linewidth=3.0, alpha=0.8, label=label1, color="red")
    plt.semilogx(freq2, dbfs2, linewidth=3.0, alpha=0.8, label=label2)

    plt.xlim(20, 24000)
    plt.ylim(-120, -40)

    # Mostra la legenda
    plt.legend()

    # Aggiungi griglia e etichette
    plt.grid(True, alpha=0.3, which='both')
    plt.grid(True, alpha=0.15, which='minor')

    plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
               ['20', '50', '100', '200', '500', '1k', '2k', '5k', '10k', '20k'])

    plt.yticks([-120, -110, -100, -90, -80, -70, -60, -50, -40],
               ['-120', '-110', '-100', '-90', '-80', '-70', '-60', '-50', '-40'])

    plt.xlabel('Frequenza (Hz)')
    plt.ylabel('Ampiezza (dBFS)')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Analisi completa. Grafico salvato in {output_file}")
    plt.close()

def process_directory_pairs(input_folder1, input_folder2, output_folder, analysis_second=7, window_size=5):
    """
    Processa coppie di file audio con lo stesso nome da due cartelle diverse.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Trova i file .wav comuni a entrambe le cartelle
    files1 = {f for f in os.listdir(input_folder1) if f.lower().endswith('.wav')}
    files2 = {f for f in os.listdir(input_folder2) if f.lower().endswith('.wav')}
    common_files = files1.intersection(files2)

    for file_name in common_files:
        input_file1 = os.path.join(input_folder1, file_name)
        input_file2 = os.path.join(input_folder2, file_name)
        output_file = os.path.join(output_folder, f"compare_{file_name.replace('.wav', '.png')}")

        print(f"Confronto: {file_name}")
        compare_audio_files(input_file1, input_file2, output_file,
                            analysis_second, window_size,
                            label1=f"Cartella 1: {file_name}",
                            label2=f"Cartella 2: {file_name}")

def compare_two_files(input_file1, input_file2, output_file, analysis_second=7, window_size=5, label1=None, label2=None):
    """
    Confronta due file audio specifici.
    """
    print(f"Confronto: {os.path.basename(input_file1)} vs {os.path.basename(input_file2)}")
    compare_audio_files(input_file1, input_file2, output_file,
                        analysis_second, window_size,
                        label1=label1 if label1 else os.path.basename(input_file1),
                        label2=label2 if label2 else os.path.basename(input_file2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Confronta file audio e genera grafici di spettro FFT sovrapposti')
    subparsers = parser.add_subparsers(dest='command', help='Comando da eseguire')

    # Parser per confrontare due file specifici
    parser_files = subparsers.add_parser('files', help='Confronta due file specifici')
    parser_files.add_argument('input_file1', type=str, help='Percorso del primo file WAV')
    parser_files.add_argument('input_file2', type=str, help='Percorso del secondo file WAV')
    parser_files.add_argument('output_file', type=str, help='Percorso del file di output PNG')
    parser_files.add_argument('--second', type=float, default=7, help='Secondo in cui eseguire l\'analisi (default: 7)')
    parser_files.add_argument('--window', type=float, default=5, help='Dimensione della finestra di analisi in secondi (default: 5)')
    parser_files.add_argument('--label1', type=str, help='Etichetta personalizzata per il primo file audio')
    parser_files.add_argument('--label2', type=str, help='Etichetta personalizzata per il secondo file audio')
    # Parser per confrontare file corrispondenti in due cartelle
    parser_dirs = subparsers.add_parser('folders', help='Confronta file corrispondenti in due cartelle')
    parser_dirs.add_argument('input_folder1', type=str, help='Percorso della prima cartella di input')
    parser_dirs.add_argument('input_folder2', type=str, help='Percorso della seconda cartella di input')
    parser_dirs.add_argument('output_folder', type=str, help='Percorso della cartella di output per i file PNG')
    parser_dirs.add_argument('--second', type=float, default=7, help='Secondo in cui eseguire l\'analisi (default: 7)')
    parser_dirs.add_argument('--window', type=float, default=5, help='Dimensione della finestra di analisi in secondi (default: 5)')

    args = parser.parse_args()

    if args.command == 'files':
        compare_two_files(args.input_file1, args.input_file2, args.output_file, args.second, args.window, args.label1, args.label2)
    elif args.command == 'folders':
        process_directory_pairs(args.input_folder1, args.input_folder2, args.output_folder, args.second, args.window)
    else:
        parser.print_help()

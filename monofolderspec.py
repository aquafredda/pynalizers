import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse
from scipy import signal as sg
from scipy.ndimage import gaussian_filter1d
import os
import warnings

def analyze_audio_file(input_file, output_file, analysis_second=7, window_size=10):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=wavfile.WavFileWarning)
        fs, original_signal = wavfile.read(input_file)
    if len(original_signal.shape) > 1:
        original_signal = np.mean(original_signal, axis=1)

    if original_signal.dtype == np.int16:
        signal = original_signal / 32768.0
    elif original_signal.dtype == np.int32:
        signal = original_signal / 2147483648.0
    elif original_signal.dtype == np.float32 or original_signal.dtype == np.float64:
        signal = original_signal
    else:
        signal = original_signal / np.iinfo(original_signal.dtype).max

    target_fs = 48000
    if fs != target_fs:
        num_samples = int(len(signal) * target_fs / fs)
        signal = sg.resample(signal, num_samples)
        fs = target_fs

    duration = len(signal) / fs
    if analysis_second >= duration:
        analysis_second = duration - window_size

    start_sample = int(analysis_second * fs)
    window_samples = int(window_size * fs)
    segment = signal[start_sample:start_sample + window_samples]

    window = sg.windows.hann(len(segment))
    segment_windowed = segment * window

    n_fft = max(16384, window_samples)
    fft_result = np.fft.rfft(segment_windowed, n=n_fft)
    freq = np.fft.rfftfreq(n_fft, d=1/fs)
    magnitude = np.abs(fft_result) / (n_fft/2)
    magnitude[1:-1] = magnitude[1:-1] * 2
    dbfs = 20 * np.log10(np.clip(magnitude, 1e-10, None))
    dbfs = gaussian_filter1d(dbfs, sigma=100)

    plt.figure(figsize=(12, 9))
    plt.semilogx(freq, dbfs, linewidth=4.0, color='black')

    # Add both grids (horizontal and vertical)
    #plt.grid(True, alpha=0.3, which='both')
    #plt.grid(True, alpha=0.15, which='minor')

    plt.xlim(20, 24000)
    # Add x-axis frequency ticks
    #plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
    #           ['20', '50', '100', '200', '500', '1k', '2k', '5k', '10k', '20k'])
    plt.xticks([])

    plt.ylim(-115, -50)
    # Add y-axis dB ticks
    #plt.yticks([-120, -110, -100, -90, -80, -70, -60, -50, -40],
    #           ['-120', '-110', '-100', '-90', '-80', '-70', '-60', '-50', '-40'])
    plt.yticks([])
    # Add labels
    #plt.xlabel('Frequency (Hz)')
    #plt.ylabel('Amplitude (dBFS)')

    # Remove only the outer frame
    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)  # Show bottom spine for x-axis
    plt.gca().spines['left'].set_visible(True)    # Show left spine for y-axis

    plt.gca().spines['top'].set_linewidth(4.0)
    plt.gca().spines['right'].set_linewidth(4.0)
    plt.gca().spines['bottom'].set_linewidth(4.0)
    plt.gca().spines['left'].set_linewidth(4.0)
    #plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Analysis complete. Plot saved to {output_file}")
    plt.close()

def process_directory(input_folder, output_folder, analysis_second=7, window_size=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith('.wav'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name.replace('.wav', '.png'))
            print(f"Processing: {file_name}")
            analyze_audio_file(input_file, output_file, analysis_second, window_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze all WAV files in a folder and generate FFT spectrum plots')
    parser.add_argument('input_folder', type=str, help='Path to the input folder containing WAV files')
    parser.add_argument('output_folder', type=str, help='Path to the output folder for saving PNG files')
    parser.add_argument('--second', type=float, default=7, help='Second at which to perform the analysis (default: 7)')
    parser.add_argument('--window', type=float, default=5, help='Analysis window size in seconds (default: 5)')

    args = parser.parse_args()
    process_directory(args.input_folder, args.output_folder, args.second, args.window)

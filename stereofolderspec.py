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

    if len(original_signal.shape) == 1:
        left_channel = right_channel = original_signal
    else:
        left_channel = original_signal[:, 0]
        right_channel = original_signal[:, 1]

    def normalize_signal(signal):
        if signal.dtype == np.int16:
            return signal / 32768.0
        elif signal.dtype == np.int32:
            return signal / 2147483648.0
        elif signal.dtype == np.float32 or signal.dtype == np.float64:
            return signal
        else:
            return signal / np.iinfo(signal.dtype).max

    left_channel = normalize_signal(left_channel)
    right_channel = normalize_signal(right_channel)

    target_fs = 48000
    if fs != target_fs:
        num_samples = int(len(left_channel) * target_fs / fs)
        left_channel = sg.resample(left_channel, num_samples)
        right_channel = sg.resample(right_channel, num_samples)
        fs = target_fs

    duration = len(left_channel) / fs
    if analysis_second >= duration:
        analysis_second = duration - window_size

    start_sample = int(analysis_second * fs)
    window_samples = int(window_size * fs)

    left_segment = left_channel[start_sample:start_sample + window_samples]
    right_segment = right_channel[start_sample:start_sample + window_samples]

    window = sg.windows.hann(len(left_segment))
    left_segment_windowed = left_segment * window
    right_segment_windowed = right_segment * window

    n_fft = max(16384, window_samples)
    freq = np.fft.rfftfreq(n_fft, d=1/fs)

    def compute_spectrum(segment):
        fft_result = np.fft.rfft(segment, n=n_fft)
        magnitude = np.abs(fft_result) / (n_fft/2)
        magnitude[1:-1] = magnitude[1:-1] * 2
        dbfs = 20 * np.log10(np.clip(magnitude, 1e-10, None))
        return gaussian_filter1d(dbfs, sigma=100)

    left_dbfs = compute_spectrum(left_segment_windowed)
    right_dbfs = compute_spectrum(right_segment_windowed)

    plt.figure(figsize=(12, 6))
    plt.semilogx(freq, left_dbfs, linewidth=3, color='blue', alpha=0.7, label='Left Channel')
    plt.semilogx(freq, right_dbfs, linewidth=3, color='red', alpha=0.7, label='Right Channel')

    plt.xlim(20, 24000)
    plt.xticks([])
    plt.ylim(-115, -50)
    plt.yticks([])

    plt.gca().spines['top'].set_visible(True)
    plt.gca().spines['right'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)
    plt.gca().spines['left'].set_visible(True)

    for spine in plt.gca().spines.values():
        spine.set_linewidth(4.0)

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

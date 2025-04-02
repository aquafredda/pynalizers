<h2>Requirements</h2>
<p>Ensure you have the required Python libraries installed. You can install them using:</p>
<pre><code>pip install numpy matplotlib scipy librosa</code></pre>

<h2>Usage</h2>

<h3>Mono Folder Spectrum Analysis (<code>monofolderspec.py</code>)</h3>
<p>Analyze all Mono WAV files in a folder and generate FFT spectrum plots</p>

<h4>Command:</h4>
<pre><code>monofolderspec.py [-h] [--second SECOND] [--window WINDOW] input_folder output_folder</code></pre>

<h4>Arguments:</h4>
<ul>
    <li><code>input_folder</code>: Path to the input folder containing WAV files.</li>
    <li><code>output_folder</code>: Path to the output folder for saving PNG files</li>
    <li><code>--second</code>: (Optional) Second at which to perform the analysis (default: 7)</li>
    <li><code>--window</code>: (Optional) Analysis window size in seconds (default: 5)</li>
</ul>

<h3>Stereoscope Visualization (<code>stereoscope.py</code>)</h3>
<p>This script generates a stereoscopic visualization from a stereo audio file.</p>

<h4>Command:</h4>
<pre><code>python3 stereoscope.py [-h] [--dpi DPI] [--markersize MARKERSIZE] [--alpha ALPHA] audio_file start_time duration output_png</code></pre>

<h4>Arguments:</h4>
<ul>
    <li><code>input.wav</code>: Path to the stereo audio file.</li>
    <li><code>start_time</code>: Start time in seconds.</li>
    <li><code>duration</code>: Duration in seconds.</li>
    <li><code>output.png</code>: Output PNG file path.</li>
</ul>

<h4>Options:</h4>
<ul>
    <li><code>-h, --help</code>: Show this help message and exit.</li>
    <li><code>--dpi DPI</code>: DPI for output image (default: 300).</li>
    <li><code>--markersize MARKERSIZE</code>: Size of plot markers (default: 0.5).</li>
    <li><code>--alpha ALPHA</code>: Alpha transparency of markers (default: 0.5).</li>
</ul>

<h2>Example</h2>
<p>To analyze a mono file:</p>
<pre><code>python monofolderspec.py audio_mono.wav output_mono.png</code></pre>

<p>To create a stereoscope visualization:</p>
<pre><code>python stereoscope.py audio_stereo.wav 5 10 output_stereo.png</code></pre>

<h2>License</h2>
<p>This project is licensed under the MIT License.</p>

<h2>Requirements</h2>
<p>Ensure you have the required Python libraries installed. You can install them using:</p>
<pre><code>pip install numpy matplotlib scipy librosa</code></pre>
<br><br>
<h2>Usage</h2>

<h3>Mono/Stereo Folder Spectrum Analysis (<code>monofolderspec.py and stereofolderspec.py</code>)</h3>
<p>Analyze all Mono/Stereo WAV files in a folder and generate FFT spectrum plots</p>

<h4>Command:</h4>
<pre><code>python3 {monofolderspec.py,stereofolderspec.py} [-h] [--second SECOND] [--window WINDOW] input_folder output_folder</code></pre>

<h4>Arguments:</h4>
<ul>
    <li><code>input_folder</code>: Path to the input folder containing WAV files.</li>
    <li><code>output_folder</code>: Path to the output folder for saving PNG files</li>
    <li><code>--second SECONDS</code>: (Optional) Second at which to perform the analysis (default: 7)</li>
    <li><code>--window WINDOW</code>: (Optional) Analysis window size in seconds (default: 5)</li>
</ul>
<br><br>
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
    <li><code>--dpi DPI</code>: DPI for output image (default: 300).</li>
    <li><code>--markersize MARKERSIZE</code>: Size of plot markers (default: 0.5).</li>
    <li><code>--alpha ALPHA</code>: Alpha transparency of markers (default: 0.5).</li>
</ul>
<br><br>

<h3>Audio Spectrum Comparison (<code>spectrumcompare.py</code>)</h3>
<p>This script compares audio files and generates overlaid FFT spectrum plots.</p>

<h4>Command:</h4>
<pre><code>python3 spectrum.py {files,folders} [options]</code></pre>

<h4>Arguments:</h4>
<ul>
    <li><code>{files,folders}</code>: Command to execute.</li>
    <li><code>files</code>: Compare two specific audio files.</li>
    <li><code>folders</code>: Compare corresponding files in two folders.</li>
</ul>

<h4>Options:</h4>
<ul>
    <li><code>--second</code>: Seconds of analysis (default: 7).</li>
    <li><code>--window</code>: Window size to analyze (default: 5).</li>
    <li><code>--label1 LABELNAME1</code>: Label for the first spectrum plot.</li>
    <li><code>--label2 LABELNAME2</code>: Label for the second spectrum plot.</li>
</ul>
<br><br>

<h3>Examples For Dummies</h3>
<pre><code>python3 monofolderspec.py thewavfolder thepngfolder
python3 stereofolderspec.py thewavfolder thepngfolder --second 10 --window 5
python3 stereoscope.py fart.wav 5 5 fart.png
python3 spectrum.py files a.wav b.wav --second 10 --window 2 --label1 "Hell" --label2 "Yeah"
python3 spectrum.py folder mygreatfolder</code></pre>
</ul>

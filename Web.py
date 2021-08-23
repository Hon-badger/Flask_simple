import os
import librosa

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt

ALLOWED_EXTENSIONS = set()
UPLOAD_FOLDER = '' # your folder
ALLOWED_EXTENSIONS.add('mp3')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            music = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            y, sr = librosa.load(music)
            n_fft = 2048
            ft = np.abs(librosa.stft(y[:n_fft], hop_length=n_fft + 1))
            plt.plot(ft)
            plt.title('Fourier Spectrum')
            plt.xlabel('Frequency Bin')
            plt.ylabel('Amplitude')
            plt.savefig('static/Fourier.jpg' + filename)
            return redirect(url_for('upload_file', filename=filename))
    return render_template('page.html')


@app.route('/Fourier')  # Набрав в адресной строке эту страницу, получаем график
def plot_fur():
    return render_template('page_img.html')


if __name__ == "__main__":
    app.run(debug=True)

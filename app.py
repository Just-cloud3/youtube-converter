from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Pagrindinis puslapis
@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST':
        # Paimame nuorodą, kurią įvedė vartotojas
        youtube_url = request.form.get('url')
        
        if youtube_url:
            try:
                # Nustatymai atsisiuntimui
                ydl_opts = {
                    'format': 'bestaudio/best', # Siunčiam geriausią audio
                    'outtmpl': 'atsisiustas_failas.%(ext)s', # Laikinas failo pavadinimas
                }
                
                # Atsisiuntimo procesas
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(youtube_url, download=True)
                    filename = ydl.prepare_filename(info)
                
                # Išsiunčiame failą vartotojui
                return send_file(filename, as_attachment=True)
            
            except Exception as e:
                message = f"Klaida: {str(e)}"
    
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

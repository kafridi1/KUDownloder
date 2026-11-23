from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return open('index.html').read()

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "No URL given"})
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return jsonify({"success": True, "link": f"/file?f={filename}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/file')
def get_file():
    f = request.args.get('f')
    if not f or not os.path.exists(f):
        return "File not found", 404
    return send_file(f, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

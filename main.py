from flask import Flask, request, Response
import cloudinary
import os
from cron import scheduler
from cron.create_video_job import IMAGE_FOLDER
from datetime import datetime


app = Flask(__name__)
scheduler.start()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@app.route("/ping")
def pong():
    return "pong"

@app.route('/live-stream', methods=['POST'])
def receive_stream():
    boundary = request.headers.get('Content-Type').split('boundary=')[-1]
    boundary = bytes(boundary, 'utf-8')

    def process_stream():
        stream_data = b""
        while True:
            chunk = request.stream.read(1000000000) # Trying the max size to all the chunk in one stream
            if not chunk:
                break
            stream_data += chunk
            while True:
                start = stream_data.find(b'--' + boundary)
                if start == -1:
                    break
                end = stream_data.find(b'--' + boundary, start + len(boundary) + 2)
                if end == -1:
                    break
                
                part = stream_data[start+len(boundary)+2:end]
                headers_end = part.find(b'\r\n\r\n')
                headers = part[:headers_end].decode()
                data = part[headers_end+4:]
                
                if "Content-Type: image/jpeg" in headers:
                    with open(f"{IMAGE_FOLDER}/image_{datetime.now().isoformat()}.jpg", 'wb') as f:
                        f.write(data)
                
                stream_data = stream_data[end+len(boundary)+2:]
        
            return Response("Stream received", status=200)

    return process_stream()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

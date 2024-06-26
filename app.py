from flask import Flask, request, jsonify
import openai
from pydub import AudioSegment

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = ""  #Add your openai api here

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Check if audio file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    audio_file = request.files['file']

    try:
        # Get the filename
        filename = audio_file.filename
        # Check if the filename ends with '.mp3'
        if filename.endswith('.mp3'):
            mp3_file = audio_file
        else:
            # Convert WAV to MP3
            audio = AudioSegment.from_file(audio_file)
            audio.export("audio.mp3", format="mp3")
            mp3_file = open("audio.mp3", "rb")
    except Exception as e:
        return jsonify({'error': f'Error converting WAV to MP3: {str(e)}'}), 500

    # Perform transcription
    try:
        transcript = openai.Audio.transcribe(
            file=mp3_file,
            model="whisper-1",
            response_format="text",
            language="en"
        )
        return jsonify({'transcript': transcript}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

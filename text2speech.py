from openai import OpenAI
import sys
from pydub import AudioSegment
import argparse
import os
import re

client = OpenAI()


def split_text(text, chunk_size=4096):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + " "

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def text_file_to_speech(input_file, voice):
    try:
        with open(input_file, 'r') as file:
            text = file.read()

        text_chunks = split_text(text)
        combined_audio = None

        for index, chunk in enumerate(text_chunks):
            chunk_file = f"chunk_{index}.mp3"
            with client.audio.speech.with_streaming_response.create(
                    model="tts-1",
                    voice=voice,
                    response_format="mp3",
                    input=chunk
            ) as response:
                with open(chunk_file, 'wb') as file:
                    for chunk in response.iter_bytes():
                        file.write(chunk)

            # Merge audio files
            chunk_audio = AudioSegment.from_mp3(chunk_file)
            combined_audio = chunk_audio if combined_audio is None else combined_audio + chunk_audio
            os.remove(chunk_file)

        output_file = os.path.splitext(input_file)[0] + ".mp3"
        combined_audio.export(output_file, format="mp3")

        print(f"Audio file created successfully: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Convert text file to speech, writing an MP3 from text.")
    parser.add_argument("input_file", help="Input text file")
    parser.add_argument("--voice", default="alloy", choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                        help="Voice selection")
    args = parser.parse_args()

    text_file_to_speech(args.input_file, args.voice)


if __name__ == "__main__":
    main()

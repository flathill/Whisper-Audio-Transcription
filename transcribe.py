import openai
import json
import os
import sys
from pydub import AudioSegment

def load_api_key(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except Exception as e:
        print(f"APIキーの読み込みエラー: {e}", file=sys.stderr)
        sys.exit(1)

def split_audio(file_path, chunk_length_ms):
    try:
        print("音声ファイルを読み込み中...")
        audio = AudioSegment.from_file(file_path, format="mp3")
        chunks = []
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunk_file_path = f"{file_path}_part{i//chunk_length_ms}.mp3"
            if not os.path.isfile(chunk_file_path):
                chunk.export(chunk_file_path, format="mp3")
                print(f"分割ファイルを作成しました: {chunk_file_path}")
            else:
                print(f"既存の分割ファイルを使用します: {chunk_file_path}")
            chunks.append(chunk_file_path)
        return chunks
    except Exception as e:
        print(f"音声ファイルの分割エラー: {e}", file=sys.stderr)
        sys.exit(1)

def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            print(f"音声ファイルを変換中: {file_path}")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript
    except Exception as e:
        print(f"音声ファイルの変換エラー: {e}", file=sys.stderr)
        return None

def save_transcript(transcript, output_file_path):
    try:
        with open(output_file_path, "w") as output_file:
            if isinstance(transcript, list):
                for t in transcript:
                    text = t.get("text", "")
                    for line in text.split('. '):
                        output_file.write(line.strip() + '.\n\n')
            else:
                text = transcript.get("text", "")
                for line in text.split('. '):
                    output_file.write(line.strip() + '.\n\n')
            print(f"変換結果を保存しました: {output_file_path}")
    except Exception as e:
        print(f"変換結果の保存エラー: {e}", file=sys.stderr)

def main():
    if len(sys.argv) != 2:
        print("使い方: python transcribe.py <音声ファイルパス>", file=sys.stderr)
        sys.exit(1)

    audio_file_path = sys.argv[1]

    if not os.path.isfile(audio_file_path):
        print(f"エラー: ファイル '{audio_file_path}' が見つかりません。", file=sys.stderr)
        sys.exit(1)

    api_key_file = "openai_api.key"
    openai.api_key = load_api_key(api_key_file)

    output_file_path = os.path.splitext(audio_file_path)[0] + "_transcript.txt"

    if os.path.isfile(output_file_path):
        print(f"変換結果ファイル '{output_file_path}' が既に存在します。処理を中断します。", file=sys.stderr)
        sys.exit(1)

    # ファイルサイズを取得し、20MBを超える場合は分割
    file_size = os.path.getsize(audio_file_path)
    chunk_length_ms = 20 * 60 * 1000  # 20分（ミリ秒単位）

    if file_size > chunk_length_ms:
        print("音声ファイルが20MBを超えているため、分割を開始します。")
        chunks = split_audio(audio_file_path, chunk_length_ms)
        full_transcript = []
        for chunk_file_path in chunks:
            transcript = transcribe_audio(chunk_file_path)
            if transcript:
                full_transcript.append(transcript)
        save_transcript(full_transcript, output_file_path)
    else:
        transcript = transcribe_audio(audio_file_path)
        if transcript:
            save_transcript(transcript, output_file_path)

if __name__ == "__main__":
    main()

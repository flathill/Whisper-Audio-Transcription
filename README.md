# Whisper Audio Transcription Script

このリポジトリは、MP3形式の音声ファイルを20MBごとに分割し、OpenAIのWhisper APIを使用して文字起こしを行うPythonスクリプトを提供します。
分割された各ファイルについて文字起こしを行い、結果を文節ごとに改行してテキストファイルに保存します。
既存の分割ファイルや文字起こし結果ファイルが存在する場合、それらを適切に処理します。

## 必要条件

このスクリプトを実行するためには、以下のソフトウェアとライブラリが必要です。

- Python 3.x
- `pydub` ライブラリ
- `ffmpeg` ソフトウェア

## インストール

1. このリポジトリをクローンします。

   ```sh
   git clone https://github.com/flathill/Whisper-Audio-Transcription.git
   cd Whisper-Audio-Transcription
   ```

2. 必要なPythonライブラリをインストールします。

   ```sh
   pip install pydub openai
   ```

3. `ffmpeg`をインストールします。以下は一般的な方法です（環境によって異なる場合があります）。

   ```sh
   sudo apt-get install ffmpeg
   ```

4. OpenAI APIキーを含むファイル `openai_api.key` を作成します。このファイルはスクリプトと同じディレクトリに配置してください。

   ```txt
   your_openai_api_key_here
   ```

## 使い方

スクリプトを実行する際に、変換対象の音声ファイルのパスを引数として渡します。

```sh
python transcribe.py <音声ファイルパス>
```

例:

```sh
python transcribe.py audio.mp3
```

### 処理の流れ

1. 指定された音声ファイルが20MBを超える場合、ファイルを約20分ごとに分割します。分割済みのファイルが既に存在する場合は、新たに分割せずにそのファイルを使用します。
2. 分割された各ファイルについてWhisper APIを使用して文字起こしを行います。
3. 文字起こし結果を文節ごとに改行してテキストファイルに保存します。
4. 文字起こしのJSONファイルが既に存在する場合、処理を中断します。

### 出力ファイル

変換結果は、元の音声ファイル名に `_transcript.txt` を付加したテキストファイルに保存されます。例として、入力ファイルが `zoom2.mp3` であれば、出力ファイルは `zoom2_transcript.txt` となります。

### エラーハンドリング

スクリプトの各ステップで発生したエラーは標準エラー出力（stderr）に出力されます。これにより、エラーメッセージを確認しやすくなっています。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、`LICENSE` ファイルを参照してください。

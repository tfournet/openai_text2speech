# openai_text2speech
Quick OpenAI Text to Speech Generator


### Usage:
```
text2speech.py [-h] [--voice {alloy,echo,fable,onyx,nova,shimmer}] input_file

Convert text file to speech, writing an MP3 from text.

positional arguments:
  input_file            Input text file

options:
  -h, --help            show this help message and exit
  --voice {alloy,echo,fable,onyx,nova,shimmer}
                        Voice selection
```

### Example:
```
export OPENAI_API_KEY='sk-13456....'
python3 ./text2speech.py --voice fable my_text.txt
Audio file created successfully: my_text.mp3
```

# Keyword extraction api

## Features

Extract keyword from text using rake and textrank

## RESTull APIs

|Description       | URL                  | METHOD | PAYLOAD             |    EXAMPLES                       |
|------------------|----------------------|--------|---------------------|-----------------------------------|
|Extract keyword using rake   | /api/rake | POST   | {text: String,      |                                   |
|                  |                      |        |  lang: String,      |                                   |
|                  |                      |        | min_char_length: Number,|                               |
|                  |                      |        | max_words_length: Number,|                              |
|                  |                      |        | min_keyword_frequency: Number}|                         |
|                  |                      |        |                     |                                   |
|Extract keyword using textrank   | /api/textrank | POST   | {text: String,      |                          |
|                  |                      |        |  lang: String}     |                                   |

## Prerequisites

In file requirements.txt

## Getting Started

```python
# Clone this project to your local.
git clone https://gitlab.com/sellpro/content/keyword-extraction
cd keyword-extraction
# Install dependency library
pip install --no-cache-dir -r requirements.txt
python app.py
```

## Todos

- Rake
  - Optimize load stopword
  - Use pos_tag to remove bad word
  - Optimize parameter
- Textrank
  - Optimize load stopword
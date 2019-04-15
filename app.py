    
from flask import Flask, request, jsonify
import pickle
import sys
sys.path.insert(0, 'rake/')
sys.path.insert(0, 'text-rank/')
import rake
import textrank
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return 'OK!'

@app.route('/api/rake',methods=['POST'])
def excute_rake():
    data = request.get_json(force=True)
    text = data['text']
    lang = data['lang']
    min_char_length = int(data['min_char_length'])
    max_words_length = int(data['max_words_length'])
    min_keyword_frequency = int(data['min_keyword_frequency'])
    stoppath = "data/stoplists/{0}.txt".format(lang)
    rake_object = rake.Rake(stoppath, min_char_length, max_words_length, min_keyword_frequency)
    print(text)
    keywords = rake_object.run(text)
    return jsonify(keywords)

@app.route('/api/textrank',methods=['POST'])
def excute_textrank():
    data = request.get_json(force=True)
    text = data['text']
    lang = data['lang']
    stoppath = "data/stoplists/{0}.txt".format(lang)
    result = textrank.extractKeyphrases_vi(text, stoppath)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
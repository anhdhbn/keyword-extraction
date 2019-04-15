from __future__ import absolute_import
from __future__ import print_function
import rake

stoppath = "../data/stoplists/vi.txt"

min_char_length = 2
max_words_length = 5
min_keyword_frequency = 4
# min_keyword_frequency tần suất xuất hiện của cụm keywork

rake_object = rake.Rake(stoppath, min_char_length, max_words_length, min_keyword_frequency)


sample_file = open("../data/docs/vi/4.txt", 'rb')
text = sample_file.read().decode("UTF-8")
keywords = rake_object.run(text)

# print(keywords)

# for k in keywords:
#     if(k[1] >= min_keyword_frequency): 
#         print(k[0], k[1])

for k in keywords:
    print(k[0], k[1])
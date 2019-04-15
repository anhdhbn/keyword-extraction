import textrank

sample_file_en = open("../data/docs/en/2.txt", 'r')
text_en = sample_file_en.read()


sample_file_vi = open("../data/docs/vi/4.txt", 'rb')
text_vi = sample_file_vi.read().decode("UTF-8")

# print(textrank.extractKeyphrases_en(text_en))
print(textrank.extractKeyphrases_vi(text_vi))
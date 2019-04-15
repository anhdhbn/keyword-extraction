import helper
import operator

def extractKeyphrases_en(text, stop_word_file="../data/stoplists/en.txt"):
    # tokenize the text using nltk
    wordTokens = helper.word_tokenize_en(text)
    # assign POS tags to the words in the text
    tagged = helper.pos_tag_en(wordTokens)
    textlist = [x[0] for x in tagged]

    

    tagged = helper.filter_for_tags_en(tagged)
    # print(tagged)
    tagged = helper.normalize(tagged)
    
    unique_word_set = helper.unique_everseen([x[0] for x in tagged])
    word_set_list = list(unique_word_set)

    # this will be used to determine adjacent words in order to construct
    # keyphrases with two words

    graph = helper.buildGraph(word_set_list)

    # pageRank - initial value of 1.0, error tolerance of 0,0001,
    calculated_page_rank = helper.pagerank(graph, weight='weight')
    # print(calculated_page_rank)
    # most important words in ascending order of importance
    keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get,
                        reverse=True)
    # print(keyphrases)
    # the number of keyphrases returned will be relative to the size of the
    # text (a third of the number of vertices)
    aThird = len(word_set_list) // 3
    # print(keyphrases)
    keyphrases = keyphrases[0:aThird + 1]
    # print(keyphrases)
    # take keyphrases with multiple words into consideration as done in the
    # paper - if two words are adjacent in the text and are selected as
    # keywords, join them together
    modifiedKeyphrases = {}
    # keeps track of individual keywords that have been joined to form a
    # keyphrase
    # Eli - modified to preserve scores for return value
    dealtWith = set([])
    i = 0
    j = 1
    while j < len(textlist):
        firstWord = textlist[i]
        secondWord = textlist[j]
        if firstWord in keyphrases and secondWord in keyphrases:
            keyphrase = firstWord + ' ' + secondWord
            modifiedKeyphrases[keyphrase] = calculated_page_rank[firstWord] + calculated_page_rank[secondWord]
            dealtWith.add(firstWord)
            dealtWith.add(secondWord)
        else:
            if firstWord in keyphrases and firstWord not in dealtWith:
                modifiedKeyphrases[firstWord] = calculated_page_rank[firstWord]

            # if this is the last word in the text, and it is a keyword, it
            # definitely has no chance of being a keyphrase at this point
            if j == len(textlist) - 1 and secondWord in keyphrases and \
                    secondWord not in dealtWith:
                modifiedKeyphrases[secondWord] = calculated_page_rank[secondWord]

        i = i + 1
        j = j + 1

    return modifiedKeyphrases

def extractKeyphrases_vi(text, stop_word_file="../data/stoplists/vi.txt"):
    text = helper.preprocess(text, stop_word_file)
    tagged = helper.pos_tag_vi(text)
    textlist = [x[0] for x in tagged]

    

    tagged = helper.filter_for_tags_vi(tagged)
    # print(tagged)
    tagged = helper.normalize(tagged)
    
    unique_word_set = helper.unique_everseen([x[0] for x in tagged])
    word_set_list = list(unique_word_set)

    # this will be used to determine adjacent words in order to construct
    # keyphrases with two words

    graph = helper.buildGraph(word_set_list)

    # pageRank - initial value of 1.0, error tolerance of 0,0001,
    calculated_page_rank = helper.pagerank(graph, weight='weight')
    # print(calculated_page_rank)
    # most important words in ascending order of importance
    keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get,
                        reverse=True)
    # print(keyphrases)
    # the number of keyphrases returned will be relative to the size of the
    # text (a third of the number of vertices)
    aThird = len(word_set_list) // 3
    # print(keyphrases)
    keyphrases = keyphrases[0:aThird + 1]
    # print(keyphrases)
    # take keyphrases with multiple words into consideration as done in the
    # paper - if two words are adjacent in the text and are selected as
    # keywords, join them together
    modifiedKeyphrases = {}
    # keeps track of individual keywords that have been joined to form a
    # keyphrase
    # Eli - modified to preserve scores for return value
    dealtWith = set([])
    i = 0
    j = 1
    while j < len(textlist):
        firstWord = textlist[i]
        secondWord = textlist[j]
        if firstWord in keyphrases and secondWord in keyphrases:
            keyphrase = firstWord + ' ' + secondWord
            modifiedKeyphrases[keyphrase] = round(calculated_page_rank[firstWord], 5) + round(calculated_page_rank[secondWord], 5)
            dealtWith.add(firstWord)
            dealtWith.add(secondWord)
        else:
            if firstWord in keyphrases and firstWord not in dealtWith:
                modifiedKeyphrases[firstWord] = round(calculated_page_rank[firstWord], 5)

            # if this is the last word in the text, and it is a keyword, it
            # definitely has no chance of being a keyphrase at this point
            if j == len(textlist) - 1 and secondWord in keyphrases and \
                    secondWord not in dealtWith:
                modifiedKeyphrases[secondWord] = round(calculated_page_rank[secondWord], 5)

        i = i + 1
        j = j + 1
    result = []
    sorted_dic = sorted(modifiedKeyphrases.items(), key=operator.itemgetter(1),reverse=True)
    for keyword in sorted_dic:
        print(keyword)
        result.append({'keyword': keyword[0], 'val': keyword[1]})
    return result

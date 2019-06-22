import pandas as pd
import pickle
import gensim
import numpy as np
import nltk
from gensim import corpora, models
from pprint import pprint
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
np.random.seed(2018)
nltk.download('wordnet')

bengali_stop_words = "অতএব অথচ অথবা অনুযায়ী অনেক অনেকে অনেকেই অন্তত অন্য অবধি অবশ্য অর্থাত আই আগামী আগে আগেই আছে আজ আদ্যভাগে আপনার আপনি আবার আমরা আমাকে আমাদের আমার আমি আর আরও ই ইত্যাদি ইহা উচিত উত্তর উনি উপর উপরে এ এঁদের এঁরা এই একই একটি একবার একে এক্ এখন এখনও এখানে এখানেই এটা এটাই এটি এত এতটাই এতে এদের এব এবং এবার এমন এমনকী এমনি এর এরা এল এস এসে ঐ ও ওঁদের ওঁর ওঁরা ওই ওকে ওখানে ওদের ওর ওরা কখনও কত কবে কমনে কয়েক কয়েকটি করছে করছেন করতে করবে করবেন করলে করলেন করা করাই করায় করার করি করিতে করিয়া করিয়ে থাকবেন থাকা থাকায় থাকে থাকেন থেকে থেকেই থেকেও দিকে দিতে দিন দিয়ে দিয়েছে দিয়েছেন দিলেন দু দুই দুটি দুটো দেওয়া দেওয়ার দেওয়া দেখতে দেখা দেখে দেন দেয় দ্বারা ধরা ধরে ধামার নতুন নয় না নাই নাকি নাগাদ নানা নিজে নিজেই নিজেদের নিজের নিতে নিয়ে নিয়ে নেই নেওয়া নেওয়ার নেওয়া নয় পক্ষে পর পরে পরেই পরেও পর্যন্ত পাওয়া পাচ পারি পারে পারেন পি পেয়ে পেয়্র্ প্রতি প্রথম প্রভৃতি প্রযন্ত প্রাথমিক প্রায় প্রায় ফলে ফিরে ফের বক্তব্য বদলে বন বরং বলতে বলল বললেন বলা বলে বলেছেন বলেন বসে হু বা বাদে বার বি বিনা বিভিন্ন বিশেষ বিষয়টি  বেশ বেশি ব্যবহার ব্যাপারে ভাবে ভাবেই মতো মতোই মধ্যভাগে মধ্যে মধ্যেই মধ্যেও মনে মাত্র মাধ্যমে মোট মোটেই যখন যত যতটা যথেষ্ট যদি যদিও যা যাঁর যাঁরা যাওয়া যাওয়ার যাওয়া যাকে যাচ্ছে যাতে যাদের যান যাবে যায় যার যারা যিনি যে যেখানে যেতে যেন যেমন র রকম রয়েছে রাখা রেখে লক্ষ শুধু শুরু সঙ্গে সঙ্গেও সব সবার সমস্ত সম্প্রতি সহ সহিত সাধারণ সামনে সি সুতরাং সে সেই".split()
bengali_stop_words = frozenset(bengali_stop_words)

data = pd.read_csv('bangla_news.csv', error_bad_lines=False)
data_text = data[['headline_text']]
a = [1,2,3]
print(type(gensim.parsing.preprocessing.STOPWORDS))

print("\n printing data text")
print(type(data_text))

data_text['index'] = data_text.index
documents = data_text


def preprocess(text):

    print("priting text length")
    print(len(text))

    result = []
    for token in text.split():
        if token not in bengali_stop_words:
            result.append(token)

    print("priting removed length \n")
    print(len(result))

    return result



print("--------------------------")
smaller_documents = documents
processed_docs = smaller_documents['headline_text'].map(preprocess)

print("printing Processed Docs\n")
print(processed_docs)


print('\npreparing and showing dictionary \n')
dictionary = gensim.corpora.Dictionary(processed_docs)
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break

print('\nPreparing BoW corpus\n')
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

bow_doc_4310 = bow_corpus[3]

for i in range(len(bow_doc_4310)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0],
                                               dictionary[bow_doc_4310[i][0]],
bow_doc_4310[i][1]))



if __name__ == '__main__':
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=6, id2word=dictionary, passes=2, workers=4)
    for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))




    unseen_document = 'সরকারের আরো একটি প্রশংসনীয় উদ্যোগের কথা জানালেন প্রধানমন্ত্রী শেখ হাসিনা। জাতীয় সংসদে প্রশ্নোত্তর পর্বে এক প্রশ্নের জবাবে তিনি বলেছেন, জনগণের স্বাস্থ্যসেবা নিশ্চিতকরণের লক্ষ্যে সরকার স্বাস্থ্যবীমা চালুর পরিকল্পনা করছে। সর্বজনীন স্বাস্থ্যসেবা নিশ্চিত করার জন্য সরকার এরই মধ্যে ‘হেলথ কেয়ার ফাইন্যান্সিং স্ট্র্যাটেজি ২০১২-২০৩২’ প্রণয়ন করেছে। পাইলট প্রকল্পের এ কৌশলে প্রাথমিকভাবে বিনা মূল্যে স্বাস্থ্যসেবা দিতে ‘স্বাস্থ্য সুরক্ষা কর্মসূচি (এসএসকে)’ শীর্ষক পাইলট প্রকল্প কার্যক্রম গ্রহণ করা হয়েছে। এসএসকের অধীন টাঙ্গাইল জেলার মধুপুর, ঘাটাইল ও কালিহাতীতে দারিদ্র্যসীমার নিচে বসবাসকারী পরিবারের সদস্যদের ৭৮টি ভর্তিযোগ্য রোগের বিনা মূল্যে সেবা দেওয়া হচ্ছে। টাঙ্গাইলের ওই তিন উপজেলা থেকে পাইলট প্রকল্পটি সংশ্লিষ্ট জেলার আরো ৯টি উপজেলায় সম্প্রসারণ কার্যক্রম শুরু করা হয়েছে জানিয়ে প্রধানমন্ত্রী বলেন, এটি সফল হলে পর্যায়ক্রমে সারা দেশে সম্প্রসারণ করা হবে।পৃথিবীর উন্নত দেশ ও কল্যাণ রাষ্ট্রগুলোয় মানুষের স্বাস্থ্যসেবা অনেকাংশে বীমার ওপর নির্ভরশীল। ফলে স্বাস্থ্যসেবা ব্যয় মেটাতে সেসব দেশের জনগণকে আর্থিক সমস্যায় পড়তে হয় না। আমাদের প্রতিবেশী দেশ ভারতে সরকারি অর্থায়নে বিশ্বের সবচেয়ে বড় স্বাস্থ্যবীমা চালু করেছে সে দেশের সরকার। গত বছর ২৫ সেপ্টেম্বর ‘আয়ুষ্মান ভারত’ নামক এ বীমা প্রকল্প কার্যকর হয়। এ বীমার আওতায় ভারতের ১০ কোটি পরিবারের অন্তত ৫০ কোটি মানুষ সুবিধা পাবে। মিলবে পাঁচ লাখ টাকা পর্যন্ত স্বাস্থ্যবীমা। সরকারি হাসপাতালের পাশাপাশি বেসরকারি হাসপাতালেও এ সুবিধা পাওয়া যাবে। হাসপাতালে ভর্তির আগে ও পরের খরচও এতে ধরা থাকবে। ভিয়েতনামে সর্বজনীন স্বাস্থ্য সুরক্ষায় গুরুত্বপূর্ণ ভূমিকা রাখছে স্বাস্থ্যবীমা কার্যক্রম। ৮৭ শতাংশ মানুষ ইউনিভার্সাল হেলথ কভারেজের (ইউএইচসি) আওতাভুক্ত। ওই দেশের প্রতিটি মানুষের জন্য রয়েছে স্বাস্থ্যবীমা সুবিধা। ধনী-দরিদ্র-নির্বিশেষে সব শ্রেণির মানুষ স্বাস্থ্যবীমার সমান সুবিধা পেয়ে থাকে।বাংলাদেশে টেকসই উন্নয়ন লক্ষ্যমাত্রা বা এসডিজির ১৭ উদ্দেশ্যের মধ্যে অন্যতম সবার জন্য সুস্বাস্থ্য। ২০৩০ সালের মধ্যে এ লক্ষ্যমাত্রা অর্জনের একটি বাধ্যবাধকতা রয়েছে। জনগণের সুস্বাস্থ্য নিশ্চিত করতে সর্বজনীন স্বাস্থ্য সুরক্ষা কর্মসূচি ও স্বাস্থ্যবীমার বিকল্প নেই। কিন্তু স্বাস্থ্যবীমা নিশ্চিত করতে প্রয়োজন সরকারি ও বেসরকারি পর্যায়ে সমন্বিত উদ্যোগ। সর্বজনীন স্বাস্থ্য সুরক্ষার ধারণায় ২০৩০ সালের মধ্যে স্বাস্থ্যসেবার ব্যয় সহনীয় পর্যায়ে ও সাধ্যের মধ্যে নিয়ে আসার কথা বলা হয়েছে। অথচ আমাদের দেশে চিকিৎসা পেতে যে পরিমাণ অর্থ ব্যয় হয়, এর ৬৭ শতাংশই রোগীকে বহন করতে হচ্ছে। সর্বজনীন স্বাস্থ্য সুরক্ষা অর্জনের জন্য মানসম্পন্ন ও দক্ষ জনবলও দরকার।আমরা আশা করব, সারা দেশে স্বাস্থ্যবীমা ছড়িয়ে দেওয়া হবে। দেশের সব শ্রেণি ও পেশার মানুষ এই বীমার আওতায় আসবে। এর ভেতর দিয়ে সত্যিকারের কল্যাণ রাষ্ট্র হওয়ার পথে অনেকটা এগিয়ে যাবে বাংলাদেশ।'
    bow_vector = dictionary.doc2bow(preprocess(unseen_document))

    for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
        print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))
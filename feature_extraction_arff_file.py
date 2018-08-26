import re
import math
import nltk
from subprocess_txala_freeling import init_subprocess

INPUT_FILE = "corpus_POS_tag"
OUTPUT_FILE = "arff_file_TFM_1708.arff"
OUTPUT_FILE_BAG_OF_WORDS = "bag_of_words_arff_TFM_1708.arff"
FIRST_MALE_TWEET = 2701
TAGS_IN_DATA_FILE = True
BAG_OF_WORDS_DICTIONARY = True
EVALUATE_UPPER_CASE_RATIO = True
PUNCTUATION_RATIO_CHARACTERS = [
    r"[-.,()¡!¿?;:0-9\"\']", r"\.", r",", r"!", r"\?", r";", r":", r"[0-9]", r"-"]
EVALUATE_MEAN_CHAR_PER_WORD = True
EVALUATE_VOCABULARY_RICHNESS = True
EVALUATE_SHORT_WORDS_RATIO = True
EVALUATE_WORD_LENGTH_STD = True
EVALUATE_WORD_LENGTH_MAX_DIFFERENCE = True
EVALUATE_HASHTAG_COUNT = True
EVALUATE_MENTION_COUNT = True
EVALUATE_EMOTE_RATIO = True
EVALUATE_TAGS = ["\\bN", "\\bV", "\\bA", "\\bRN", "\\bRG", "\\bP"]
EVALUATE_DICTIONARIES = ["curse_words_cat", "stop_words_cat",
                         "polar_words_positive_cat", "polar_words_negative_cat"]
EVALUATE_BAG_OF_WORDS = True
EVALUATE_TREE_MEASURES = ["TREE_NUMBER_OF_SENTENCES", "TREE_WIDTH_MEAN", "TREE_HEIGHT_MEAN"]
FORMAT_STRING = "{: 9.5f}"
CHARACTERS_NOT_TO_TAGGENIZE = r'[#@\U0001F000-\U0001F0FF\U0001F300-\U0001F9FF]'
TAG_RE = r"^\S+\s\S+\s(\b[\w]+\b).*$"
TAG_SUB = r"\1"


def _phrase_to_word_list(cad):
    re.sub(r" {2,}", " ", cad)
    return re.split(r" ", cad)

def tokenize_line(cleaned_line):
    lowercase_lines = cleaned_line.lower()
    tokenized_lines = nltk.word_tokenize(lowercase_lines, language= 'spanish')
    #print(lowercase_lines)
    return tokenized_lines

def clean_line(cad):
    cad = cad.strip()

    cad = re.sub(r'…', '', cad)

    if re.search(r'^$', cad):
        print("Linea vacia")
        return ""

    if re.search(r'^RT', cad):
        print("Retweet:", repr(cad))
        return ""
    cad = re.sub(r'(https?:\/\/|www\.)(\S*)?', '', cad)
    cad = cad.strip()
    return cad


def get_cleaned_line(line):
    cleaned_line = clean_line(line)
    cleaned_line = re.sub(r"^[\w,]*:::(.*)$", r"\1", cleaned_line)
    cleaned_line = cleaned_line.replace(r"@", '').replace(r"#", '')
    cleaned_line = cleaned_line.replace(r"`", '')
    return cleaned_line


def upper_ratio(cad):
    return len(re.findall(r"[A-Z]", cad)) / len(cad)


def punct_ratio(cad, regex):
    return len(re.findall(regex, cad)) / len(cad)


def mean_char_per_word(cad):
    words = tokenize_line(cad)
    sum = 0
    for word in words:
        sum += len(word)
    return sum / len(words)


def richness(cad):
    words = tokenize_line(cad)
    return len(set(words)) / len(words)


def shortwords_ratio(cad):
    words = tokenize_line(cad)
    count = 0
    for word in words:
        if len(word) > 1 and len(word) < 4:
            count += 1
    return count / len(words)


def std_word_length(cad):
    words = tokenize_line(cad)
    sum = 0
    for word in words:
        sum += len(word)
    mean = sum / len(words)
    err = 0
    for word in words:
        err += (len(word) - mean) ** 2
    return math.sqrt(err)


def max_word_len_dif(cad):
    words = tokenize_line(cad)
    shortest = 50
    longest = 0
    length = 0
    for word in words:
        length = len(word)
        if length < shortest:
            shortest = length
        if length > longest:
            longest = length
    if longest < shortest:
        return 0
    return longest - shortest


def hashtag_count(cad):
    words = tokenize_line(cad)
    return len(re.findall(r'\s#\w+', cad)) / len(words)


def mention_count(cad):
    words = tokenize_line(cad)
    return len(re.findall(r"\s@\w+", cad)) / len(words)


def emote_ratio(cad):
    return len(re.findall(r'[\U0001F000-\U0001F0FF\U0001F300-\U0001F9FF]', cad)) / len(cad)


def count_dictionary(cad, word_file):
    dictionary_content = ""
    words = tokenize_line(cad)
    with open(word_file, encoding="utf8") as f:
        dictionary_content = ",".join(f.readlines())
        dictionary_content = re.sub(r",+ ?", ",", dictionary_content)
    return count_occurrences(cad, dictionary_content.split(",")) / len(words)


def count_occurrences(cad, word_list):
    regex = re.sub("([\][(){}\\+*^$.'\"])", "\\\1", "|".join(word_list))
    return len(re.findall(regex, cad, flags=re.I))


def taggenize_tweet(cad):
    cad = re.sub(CHARACTERS_NOT_TO_TAGGENIZE, '', cad)
    analyzer_output = analyzer.communicate(input=cad.encode())[0].decode()
    tags = []
    for line in analyzer_output.split("\n"):
        if re.match(r"^\s*$", line):
            continue
        tags.append(re.sub(TAG_RE, TAG_SUB, line))
    return "\n".join(tags)


def get_input_file_content():
    with open(INPUT_FILE, encoding="utf8") as f:
        return f.readlines()[:100]


def get_all_unique_words_list(input_file_content):
    all_unique_words_list = []
    for line in input_file_content:
        cleaned_line = get_cleaned_line(line)
        words_in_line = tokenize_line(cleaned_line)
        for word in words_in_line:
            if re.search(r'[^$^a-zA-z`]', word) or len(word) > 3 or word in all_unique_words_list:
                continue
            all_unique_words_list.append(word)
    return all_unique_words_list


def bag_of_words(input_file_content, number_of_different_words):
    bag_of_words = []
    for tweet in input_file_content:
        cleaned_tweet = get_cleaned_line(tweet)
        tweet_words = tokenize_line(cleaned_tweet)
        tweet_words_cleaned = get_clean_list_words(tweet_words)
        tweet_words_counters = [0] * number_of_different_words
        for word in tweet_words_cleaned:
            if re.search(r'[^$^a-zA-z]', word) or len(word) > 3 or word not in all_unique_words_list:
                continue
            tweet_words_counters[all_unique_words_list.index(word)] += 1
        bag_of_words.append(tweet_words_counters)
    return bag_of_words


def evaluate_traits(cad, etiq):
    traits = []
    if (EVALUATE_UPPER_CASE_RATIO):
        traits.append(FORMAT_STRING.format(upper_ratio(cad)))
    if (PUNCTUATION_RATIO_CHARACTERS):
        for regex in PUNCTUATION_RATIO_CHARACTERS:
            traits.append(FORMAT_STRING.format(punct_ratio(cad, regex)))
    if (EVALUATE_TAGS):
        etiquetas = ""
        if not TAGS_IN_DATA_FILE:
            print("ALERTA TAGGING")
            etiquetas = taggenize_tweet(cad)
        else:
            etiquetas = re.sub(",", "\n", etiq)
        for item in EVALUATE_TAGS:
            traits.append(FORMAT_STRING.format(
                count_occurrences(etiquetas, [item]) / len(etiquetas)))
    if EVALUATE_MEAN_CHAR_PER_WORD:
        traits.append(FORMAT_STRING.format(mean_char_per_word(cad)))
    if EVALUATE_VOCABULARY_RICHNESS:
        traits.append(FORMAT_STRING.format(richness(cad)))
    if EVALUATE_SHORT_WORDS_RATIO:
        traits.append(FORMAT_STRING.format(shortwords_ratio(cad)))
    if EVALUATE_WORD_LENGTH_STD:
        traits.append(FORMAT_STRING.format(std_word_length(cad)))
    if EVALUATE_WORD_LENGTH_MAX_DIFFERENCE:
        traits.append(FORMAT_STRING.format(max_word_len_dif(cad)))
    if EVALUATE_HASHTAG_COUNT:
        traits.append(FORMAT_STRING.format(hashtag_count(cad)))
    if EVALUATE_MENTION_COUNT:
        traits.append(FORMAT_STRING.format(mention_count(cad)))
    if EVALUATE_EMOTE_RATIO:
        traits.append(FORMAT_STRING.format(emote_ratio(cad)))
    if EVALUATE_DICTIONARIES:
        for item in EVALUATE_DICTIONARIES:
            traits.append(FORMAT_STRING.format(count_dictionary(cad, item)))
    if EVALUATE_TREE_MEASURES:
        sentence_counter = 0
        width_counter = 0
        height_counter = 0
        for sentence_measures in init_subprocess(cad):
            sentence_counter = sentence_measures[0]
            width_counter += sentence_measures[1]
            height_counter += sentence_measures[2]
        traits.append(FORMAT_STRING.format(sentence_counter))
        traits.append(FORMAT_STRING.format(width_counter/sentence_counter))
        traits.append(FORMAT_STRING.format(height_counter/sentence_counter))
    return traits


def evaluate_bag_of_words_traits(all_unique_words_list, bag_of_words, counter):
    traits = []
    if (EVALUATE_BAG_OF_WORDS):
        for word in all_unique_words_list:
            traits.append(FORMAT_STRING.format(
                bag_of_words[counter][all_unique_words_list.index(word)]))
    return traits


def get_trait_def():
    trait_def = []
    if (EVALUATE_UPPER_CASE_RATIO):
        trait_def.append('"Uppercase ratio"\t\tNUMERIC')
    if (PUNCTUATION_RATIO_CHARACTERS != []):
        for item in PUNCTUATION_RATIO_CHARACTERS:
            trait_def.append('"Punctuation ratio of ' + item + '"\t\tNUMERIC')
    if (EVALUATE_TAGS != []):
        for item in EVALUATE_TAGS:
            trait_def.append('"Tag ratio of ' + item + '"\t\tNUMERIC')
    if (EVALUATE_MEAN_CHAR_PER_WORD):
        trait_def.append('"Mean chars per word"\tNUMERIC')
    if (EVALUATE_VOCABULARY_RICHNESS):
        trait_def.append('"Vocabulary richness"\tNUMERIC')
    if (EVALUATE_SHORT_WORDS_RATIO):
        trait_def.append('"Short words ratio"\t\tNUMERIC')
    if (EVALUATE_WORD_LENGTH_STD):
        trait_def.append('"Word length STD"\t\tNUMERIC')
    if (EVALUATE_WORD_LENGTH_MAX_DIFFERENCE):
        trait_def.append('"Max word length difference"\tNUMERIC')
    if (EVALUATE_HASHTAG_COUNT):
        trait_def.append('"Hashtag count"\t\tNUMERIC')
    if (EVALUATE_MENTION_COUNT):
        trait_def.append('"Mention count"\t\tNUMERIC')
    if (EVALUATE_EMOTE_RATIO):
        trait_def.append('"Emote ratio"\t\tNUMERIC')
    if (EVALUATE_DICTIONARIES != []):
        for item in EVALUATE_DICTIONARIES:
            trait_def.append('"Word ocurrence from ' + item + '"\t\tNUMERIC')
    if EVALUATE_TREE_MEASURES:
        for measure in EVALUATE_TREE_MEASURES:
            trait_def.append('"' + measure + '"\t\tNUMERIC')
    trait_def.append('"Gender"\t\t\t\t{female,male}')
    return trait_def


def get_trait_list():
    count = 1
    gender = "female"
    trait_list = []
    for it in get_input_file_content():
        if count == FIRST_MALE_TWEET:
            gender = "male"
        count += 1
        if count % 250 == 0:
            print("Procesando tweet ", count)
        etiquetas = ""
        if (TAGS_IN_DATA_FILE):
            etiquetas = re.sub(r"^([\w,]*):::.*$", r"\1", it)
        item = re.sub(r"^[\w,]*:::(.*)$", r"\1", it)
        itemc = clean_line(item)
        if re.search(r'^$', itemc):
            continue
        traits = evaluate_traits(itemc, etiquetas)
        traits.append(gender)
        trait_list.append(",".join(traits))
    return trait_list


def get_trait_bag_of_words_def():
    trait_def = []
    if (EVALUATE_BAG_OF_WORDS):
        all_unique_words_list_cleaned = get_clean_list_words(
            all_unique_words_list)
        for word in all_unique_words_list_cleaned:
            trait_def.append('"Ocurrences of ' + word + '"\t\tNUMERIC')
    trait_def.append('"Gender"\t\t\t\t{female,male}')
    return trait_def


def get_trait_bag_of_words_list(all_unique_words_list, bag_of_words):
    count = 1
    counter = 0
    gender = "female"
    trait_list = []
    for tweet in get_input_file_content():
        if count == FIRST_MALE_TWEET:
            gender = "male"
        count += 1
        if count % 250 == 0:
            print("Procesando tweet ", count)
        traits = evaluate_bag_of_words_traits(
            all_unique_words_list, bag_of_words, counter)
        counter += 1
        traits.append(gender)
        trait_list.append(",".join(traits))
    return trait_list


def write_arff():
    output_file = open(OUTPUT_FILE, "w", encoding="utf8")
    output_file.write("@relation tweets\n\n")

    for i in get_trait_def():
        output_file.write("@attribute %s\n" % i)
    output_file.write("\n")

    output_file.write("@DATA\n")
    for tweet in get_trait_list():
        output_file.write(tweet)
        output_file.write("\n")


def write_bag_of_words_arff(all_unique_words_list, bag_of_words):
    output_file = open(OUTPUT_FILE_BAG_OF_WORDS, "w", encoding="utf8")
    output_file.write("@relation tweets\n\n")

    for i in get_trait_bag_of_words_def():
        output_file.write("@attribute %s\n" % i)
    output_file.write("\n")

    output_file.write("@DATA\n")
    for tweet in get_trait_bag_of_words_list(all_unique_words_list, bag_of_words):
        output_file.write(tweet)
        output_file.write("\n")


def get_clean_list_words(words):
    clean_list_words = []
    for word in words:
        cleaned_word = re.sub(r"\b[^a-zA-Z]+", "", word)
        cleaned_word = re.sub(r"[^a-zA-Z]+\b", "", cleaned_word)
        clean_list_words.append(cleaned_word)
    return clean_list_words


all_unique_words_list = get_all_unique_words_list(get_input_file_content())
bag_of_words = bag_of_words(get_input_file_content(), len(all_unique_words_list))
write_bag_of_words_arff(all_unique_words_list, bag_of_words)

write_arff()
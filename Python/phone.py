phone_number = {
    '0': [''],
    '1': [''],
    '2': ['a','b','c'],
    '3': ['d','e','f'],
    '4': ['g','h','i'],
    '5': ['j','k','l'],
    '6': ['m','n','o'],
    '7': ['p','q','r','s'],
    '8': ['t','u','v'],
    '9': ['w','x','y','z']
}

def generate_all_possible_words(number):
    words = []
    for c in number:
        r = []
        if len(words) == 0:
            r = phone_number[c]
        else:
            for l in phone_number[c]:
                result = add_character_to_word(l, words)
                r.extend(result)
        words = r
    return words


def add_character_to_word(character, words):
    result = []
    for word in words:
        word = "%s%s" % (word, character)
        result.append(word)
    return result


def load_dictionary():
    f = open('/usr/share/dict/words', 'r')
    d = {}
    for line in f:
        d[line[:-1]] = line 
    f.close()
    return d


def filter_real_worlds(words):
    dict = load_dictionary()
    result = []
    for word in words:
        if word in dict:
            result.append(word)
    return result


if __name__ == '__main__':
    phone = '6666'
    #phone = '3254773'
    words = generate_all_possible_words(phone)
    result = filter_real_worlds(words)
    print result


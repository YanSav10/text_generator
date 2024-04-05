import random


def read_corpus(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        tokens = text.split()
        return tokens


def create_trigrams_model(tokens):
    trigrams = [(tokens[i] + ' ' + tokens[i + 1], tokens[i + 2]) for i in range(len(tokens) - 2)]
    model = {}
    for head, tail in trigrams:
        if head not in model:
            model[head] = {}
        if tail not in model[head]:
            model[head][tail] = 1
        else:
            model[head][tail] += 1
    return model


def is_valid_starting_head(head):
    first_word = head.split()[0]
    return first_word[0].isupper() and not first_word[-1] in ".!?"


def generate_chain(model, min_length=5):
    valid_heads = [head for head in model.keys() if is_valid_starting_head(head)]
    current_head = random.choice(valid_heads)
    chain = current_head.split(' ')

    while True:
        if current_head not in model or not model[current_head]:
            break

        next_words = model[current_head]
        next_word = max(next_words, key=next_words.get)
        chain.append(next_word)
        current_head = ' '.join(chain[-2:])

        if len(chain) >= min_length and chain[-1][-1] in ".!?":
            break

    return ' '.join(chain)


if __name__ == "__main__":
    file_input = input()
    token = read_corpus(file_input)
    trigrams_model = create_trigrams_model(token)

    for _ in range(10):
        sentence = generate_chain(trigrams_model)
        print(sentence)

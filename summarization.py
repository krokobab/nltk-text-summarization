# Импортируем библиотеку nltk, корпус стоп-слов, функции для токенизации текста
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


# Объявляем функцию суммаризации
def summarize(text, compression_parameter):
    # Токенизируем текст
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Создаём переменные для хранения множества стоп-слов, а также стеммера
    stopwords_set = set(stopwords.words("russian"))
    stemmer = nltk.PorterStemmer()
    # Производим стемминг текста, а также его фильтрацию от стоп-слов
    filtered_words = [stemmer.stem(word) for word in words if word.lower() not in stopwords_set and word.isalnum()]
    # Создаём таблицу частоты употребления слов в тексте
    freq_table = dict()
    # Заполняем её
    for word in filtered_words:
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1
    # Создаём таблицу числовых значений для каждого предложения (на основе частоты употребления слов, встречающихся в
    # предложении)
    sentence_value = dict()
    # Заполняем её
    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq
    # Вычисляем среднее арифметическое всех числовых значений предложений
    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]

    avg = int(sum_values / len(sentence_value))
    # Создаём переменную для хранения итогового резюме
    summary = ""
    # Отбираем предложения, которые попадут в итоговое резюме, сравнивая числовое значение, соответствующее каждому
    # из них, со средним арифметическим, умноженным на параметр сжатия, передающийся пользователем
    while summary == "":
        for sentence in sentences:
            if sentence in sentence_value and sentence_value[sentence] > compression_parameter * avg:
                summary += " " + sentence
        compression_parameter -= 0.1
    # Возвращаем получившееся резюме
    return summary

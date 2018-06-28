import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


def _calculate_languages_ratios(text):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

    @param text: Text whose language want to be detected
    @type text: str

    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """

    languages_ratios = {}

    '''
    nltk.wordpunct_tokenize() splits all punctuations into separate tokens

    >>> wordpunct_tokenize("That's thirty minutes away. I'll be there in ten.")
    ['That', "'", 's', 'thirty', 'minutes', 'away', '.', 'I', "'", 'll', 'be', 'there', 'in', 'ten', '.']
    '''

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)  # language "score"

    return languages_ratios


def detect_language(text):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.

    It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.

    @param text: Text whose language want to be detected
    @type text: str

    @return: Most scored language guessed
    @rtype: str
    """

    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language


if __name__=='__main__':

    text = '''
    Es gibt eine Stelle, die ich auswendig gelernt habe. Hesekiel 25:17. "Der Weg des rechten Mannes ist auf allen Seiten belagert \
    von den Missetaten des Selbstsüchtigen und der Tyrannei der Bösen. Gesegnet sei er, der im Namen der Nächstenliebe
    und der gute Wille, verdammt die Schwachen durch das Tal der Finsternis, denn es ist wirklich der Hüter seines Bruders
    und der Sucher von verlorenen Kindern. Und ich werde dich mit großer Rache und wütender Wut schlagen
    diejenigen, die versuchen, meine Brüder zu vergiften und zu zerstören. Und du wirst wissen, dass ich der Herr bin, wenn ich mich räche
    über dich. "Nun ... ich habe diesen Scheiß jahrelang gesagt und wenn ich es jemals gehört habe, hat das deinen Arsch bedeutet.
    Um tot zu sein, habe ich nie wirklich darüber nachgedacht, was es bedeutet. Ich dachte, es war ein kaltblütiges Ding
    zu einem Hurensohn zu sagen, bevor ich eine Kappe in seinen Arsch zog. Aber ich sah ein paar Dinge, die mich heute Morgen zum Nachdenken brachten
    zweimal. Siehst du, jetzt denke ich: Vielleicht bedeutet es, dass du der böse Mann bist. Und ich bin der Richtige. Und Herr
    9mm hier ... es ist der Hirte, der meinen rechten Hintern im Tal der Dunkelheit schützt. Oder es könnte bedeuten \
    Du bist der Gerechte und ich bin der Pastor und es ist die Welt, die böse und selbstsüchtig ist. Und ich möchte \
    dass. Aber diese Scheiße ist nicht die Wahrheit. Die Wahrheit ist, dass du der Schwache bist. Und ich bin die Tyrannei der bösen Menschen.
    Aber ich versuche es, Ringo. Ich versuche wirklich, der Pastor zu sein.
    '''

    print(detect_language(text))


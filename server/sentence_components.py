import nltk

class Sentence:
    class Component:
        def __init__(self, word, tag):
            self.words = [word]
            if tag == 'PRP':
                self.comp = 'S' if word.lower() in ['i', 'you', 'he', 'she', 'it', 'we', 'they'] else 'O'
            elif tag.startswith('NN'): self.comp = 'SO'
            elif tag.startswith('VB') or tag == 'MD': self.comp = 'P'
            else: self.comp = None
            
        def add_words(self, words):
            self.words += words
        
        def log(self):
            print(f'{self.comp}: {self.words}')


    class Triplet:
        def __init__(self, subject=None, predicate=None, obj=None):
            self.subject = subject
            self.predicate = predicate
            self.obj = obj
        
        def log(self):
            print(f'S: {self.subject}, P: {self.predicate}, O:{self.obj}')


    def __init__(self, phrase):
        self.txt = phrase
        self.triplets = self.__triplets(self.__unified_comps(self.__comps(self.txt)))

    def __comps(self, txt):
        tokenized = nltk.word_tokenize(txt)
        comps = list()
        for word, tag in nltk.pos_tag(tokenized):
            sc = Sentence.Component(word, tag)
            if sc.comp:
                comps.append(sc)
        return comps
    
    def __unified_comps(self, comps):
        unified = list()
        current_comp = None
        for comp in comps:
            if comp.comp == current_comp:
                unified[-1].add_words(comp.words)
            else:
                current_comp = comp.comp
                unified.append(comp)
        return unified
    
    def __triplets(self, comps):
        subject = None
        triplets = list()
        for comp in comps:
            if subject == None:
                if 'S' in comp.comp:
                    subject = comp.words
                continue
            if comp.comp == 'P':
                triplets.append(Sentence.Triplet(subject, comp.words))
                continue
            if 'O' in comp.comp and triplets:
                triplets[-1].obj = comp.words
        return triplets
            

    def log(self):
        print(self.txt)
        for t in self.triplets:
            t.log()


class Text:
    def __init__(self, txt):
        self.txt = txt
        self.sentences = [
            Sentence(phrase) for phrase in nltk.sent_tokenize(txt)
        ]
    
    def log(self):
        for s in self.sentences:
            s.log()
            print('')


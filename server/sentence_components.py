import nltk

class Sentence:
    # https://www.wordy.com/writers-workshop/basic-english-sentence-structure/
    # https://academicguides.waldenu.edu/writingcenter/grammar/sentencestructure
    #
    # according to this, we can already identify 5 different simple sentence structures, mostly 3-tuples
    # and 3 different ways of building long sentences: simple, compound, complex
    # for complex clauses, we should try do identify the dependent clauses by the absence of subjects in them
    # (subject is before predicate in an active clause), the rest would be a piece of cake.
    # I propose splitting the sentences by commas, then identifying each clause as either independent clause or dependent.
    # Afterwards, check if the independent clauses fit one of the 5 patterns, if the clause is dependent, add the previous subject to the 3-tuples.
    
    # One problem is that a complex sentence where the independent clause comes first doesnt have a comma.
    # Proposed solution: deciding between active/passive clause & searching for a subject before the predicate.
    # If no subject is given, it's a dependent clause.
    
    class Crux:

        __candidates = {
            'subject': ["NN", "NNS", "NNP", "NNPS", "PRP"],
            'object': [],
            'predicate': ["MD", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"],
            'adjective': ["JJ", "JJR", "JJS"],
            'adverb': ["RB", "RBR", "RBS"],
        }
    
        def __init__(self, tuples):
            self.tuples = tuples
            self.atts = {
                pos: [n for n, t in enumerate(self.tuples) if t[1] in candidates]
            for pos, candidates in Sentence.Crux.__candidates.items()}
            # normaler hauptsatz: subject candidates vor pradikat gehoren zum subject, der rest zum objekt
            # wenn kein pradikat zwischen subjekt kandidaten, dann vermutlich nebensatz -> subj kandidaten sind ein objekt
            self.independent = bool(self.atts['subject'] and [idx for idx in self.atts['predicate'] if idx in range(self.atts['subject'][0], self.atts['subject'][-1])])
            if self.independent:
                subj_c = self.atts['subject']
                self.atts['subject'] = []
                for idx in subj_c:
                    if idx < self.atts['predicate'][0]: self.atts['subject'].append(idx)
                    else: self.atts['object'].append(idx)
            else:
                self.atts['object'] = self.atts['subject']
                self.atts['subject'] = []
        
        def log(self):
            print([t[0] for t in self.tuples])
            print({k: [self.tuples[i][0] for i in v] for k, v in self.atts.items()})
    
    __phrase_split_tags = ['CC', 'IN', 'LS', 'WDT', 'WP']

    def __init__(self, phrase):
        self.txt = phrase.replace('can\'t', 'cannot').replace('won\'t', 'will not').replace('n\'t', ' not')
        self.subphrases = self.txt.split(',')
        sp_tuples = [nltk.pos_tag(nltk.word_tokenize(sp)) for sp in self.subphrases]
        tuples = list()
        for spt in sp_tuples:
            split_idcs = [0] + [n for n, t in enumerate(spt) if t[1] in Sentence.__phrase_split_tags] + [len(spt) - 1]
            tuples += [
                spt[split_idcs[n]:split_idcs[n + 1]]
            for n in range(len(split_idcs[:-1]))]
            
        self.cruxes = [Sentence.Crux(t) for t in tuples]

    def log(self):
        print(self.txt)
        for c in self.cruxes:
            c.log()

class Text:
    def __init__(self, txt):
        self.txt = txt
        self.sentences = [
            Sentence(phrase) for phrase in nltk.sent_tokenize(txt)
        ]
    
    def log(self):
        for s in self.sentences:
            s.log()
            print()


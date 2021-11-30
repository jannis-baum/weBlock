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
    
    
    # some helper methods for nltk pos tag lists that I don't want to retype all the time
    def __subject_candidates(self):
        return ["NN", "NNS", "NNP", "NNPS", "PRP"]
    
    def __predicate_candidates(self):
        return ["MD", "VB", "VBD", "VBG", "VBN", "VBP", "VPZ"]
    
    def __adjective_candidates(self):
        return ["JJ", "JJR", "JJS"]
    
    def __adverb_candidates(self):
        return ["RB", "RBR", "RBS"]
    
    
    
    # this method takes an identified independent clause and greedily tries to fill
    # a triplet in the case that it is a type 1 independent clause
    # type 1: subject-verb
    # our component class is too restrictive for this, so these methods use the tuples that are returned by nltk.tokenize()
    def __independent_clause_1(self, tuples):
        subject = None
        predicate = []
        
        for tup in tuples:
            if subject == None:
                if tup[1] in self.__subject_candidates():
                    subject = tup[0]
            if tup[1] in self.__predicate_candidates():
                predicate.append(tup[0])
        return Triplet(subject, predicate)
    
    # takes an identified independent clause and greedily tries to fill
    # a triplet in the case that it is a type 2 independent clause:
    # type 2: subject-verb-object
    def __independent_clause_2(self, tuples):
        subject = None
        predicate = []
        #maybe the obj should be a single word but for now let's test it with a list of objects
        obj = []
        
        for tup in tuples:
            if subject == None:
                if tup[1] in self.__subject_candidates():
                    subject = tup[0]
            if tup[1] in self.__predicate_candidates:
                predicate.append(tup[0])
            if subject != None and tup[1] in self.__subject_candidates():
                obj.append(tup[0])
        
        return Triplet(subject, predicate, obj)
    
    # type 3: subject-verb-adjective
    # this is where our triplet class has it's issues - of course the adjective/adverb can be critical or uncritical of the regime...
    # returning a tuple of the three parts-of-speech for now
    def __independent_clause_3(self, tuples):
        subject = None
        predicate = []
        adjective = None
        
        for tup in tuples:
            if subject == None:
                if tup[1] in self.__subject_candidates():
                    subject = tup[0]
            if tup[1] in self.__predicate_candidates():
                predicates.append(tup[0])
            if adjective == None:
                if tup[1] in self.__adjective_candidates():
                    adjective = tup[0]
        return (subject, predicate, adjective)
            

    # type 4: subject-verb-adverb
    def __independent_clause_4(self, tuples):
        subject = None
        predicate = []
        adverb = None
        
        for tup in tuples:
            if subject == None:
                if tup[1] in self.__subject_candidates():
                    subject = tup[0]
            if tup[1] in self.__predicate_candidates():
                predicates.append(tup[0])
            if adjective == None:
                if tup[1] in self.__adverb_candidates():
                    adverb = tup[0]
        return (subject, predicate, adverb)
    
    # type 5: subject-verb-noun
    def __independent_clause_5(self, tuples):
        subject = None
        predicate = []
        noun = None
        
        for tup in tuples:
            if subject == None:
                if tup[1] in self.__subject_candidates():
                    subject = tup[0]
            if tup[1] in self.__predicate_candidates():
                predicates.append(tup[0])
            if subject != None and noun == None:
                # a noun shouldn't be a personal pronoun
                if tup[1] in ["NN", "NNS", "NNP", "NNPS"]:
                    noun = tup[0]
        return (subject, predicate, noun)
    
    # takes an identified passive clause and greedily tries to fill
    # a triplet with the subject parameter and the predicate + object/adjective/adverb from the clause
    # don't know how many different types there are yet
    def __passive_clause_1(self, tuples, subject):
        pass
    
    # not sure if the comps can help with this yet. 
    # takes a sentence (and perhaps it's comps) and splits the sentence into it's
    # individual clauses, by splitting at commas and conjunctions (CC tag in nltk)
    # each individual clause can then be processed by the clause methods
    # returns lists of nltk-tag-lists (which I call tuples because fuck you)
    def __split_sentence(self, tuples, sentence):
        pass
    
    
    # this is a prototype just to show how I imagined the sentence evaluation. the method probably belongs in the page_processor
    def __evaluate_sentence(self, sentence)
        tuples = nltk.sent_tokenize(sentence)
        clauses = self.__split_sentence(tuples, sentence)
        #the information stored in triplet form
        aspects = []
        
        censoring = False
        # this is where our customization comes into play
        protected_actor_list = []
        protected_action_list = []
        # a bonus in case we want interactions with a specific actor to be censored in all cases
        shit_list = []
        
        for clause in clauses:
            it1 = self.__independent_clause_1(clause)
            #...same for types 2-5 and dependent clauses
            
            # likely that the clause is an independent clause type 1
            # of course, one clause can fit multiple types, we can solve this by either prioritizing one clause type over another, or thinking of something else...
            if None not in it1:
                aspects.append(it1)
                continue
        
        # assuming that aspects are 3-tuples like in __independent_clause_4 (but we can exchange it with a new class)
        for aspect in aspects:
            if aspect[0] in protected_actor_list:
                if aspect[1] in protected_action_list:
                    censoring = True
                if aspect[2] in shit_list:
                    censoring = True
        
        return censoring
        

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


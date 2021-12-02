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
        def __init__(self, actor=None, action=None, target=None, modifier=None):
            self.actor = actor
            self.action = action
            self.target = target
            self.modifier = modifier
        
        def value(self):
            v = 0
            if self.actor: v += 1
            if self.action: v += len(self.action)
            if self.target: v += len(self.target)
            if self.modifier: v += 1
            return v
        
        def log(self):
            print(f'{self.actor} {self.action} {self.target} {self.modifier}')


    def __init__(self, phrase):
        self.txt = phrase
        self.__evaluate()

    def log(self):
        print(self.txt)
        self.crux.log()

    # some helper properties for nltk pos tag lists that I don't want to retype all the time
    __subject_candidates = ["NN", "NNS", "NNP", "NNPS", "PRP"]
    __predicate_candidates = ["MD", "VB", "VBD", "VBG", "VBN", "VBP", "VPZ"]
    __adjective_candidates = ["JJ", "JJR", "JJS"]
    __adverb_candidates = ["RB", "RBR", "RBS"]
    
    # this method takes an identified independent clause and greedily tries to fill
    # a triplet in the case that it is a type 1 independent clause
    # type 1: subject-verb
    # our component class is too restrictive for this, so these methods use the tuples that are returned by nltk.tokenize()
    def __independent_clause_1(self, tuples):
        subject = None
        predicate = []
        
        for tup in tuples:
            if subject == None:
                if tup[1] in Sentence.__subject_candidates:
                    subject = tup[0]
            if tup[1] in Sentence.__predicate_candidates:
                predicate.append(tup[0])
        return Sentence.Crux(subject, predicate)
    
    # takes an identified independent clause and greedily tries to fill
    # a triplet in the case that it is a type 2 independent clause:
    # type 2: subject-verb-object
    def __independent_clause_2(self, tuples):
        subject = None
        predicate = []
        #maybe the obj should be a single word but for now let's test it with a list of objects
        obj = []
        
        for tup in tuples:
            if subject != None and tup[1] in Sentence.__subject_candidates:
                obj.append(tup[0])
            if subject == None:
                if tup[1] in Sentence.__subject_candidates:
                    subject = tup[0]
            if tup[1] in Sentence.__predicate_candidates:
                predicate.append(tup[0])
        
        return Sentence.Crux(subject, predicate, obj)
    
    # type 3: subject-verb-adjective
    # this is where our triplet class has it's issues - of course the adjective/adverb can be critical or uncritical of the regime...
    # returning a tuple of the three parts-of-speech for now
    def __independent_clause_3(self, tuples):
        subject = None
        predicate = []
        adjective = None
        
        for tup in tuples:
            if subject == None:
                if tup[1] in Sentence.__subject_candidates:
                    subject = tup[0]
            if tup[1] in Sentence.__predicate_candidates:
                predicate.append(tup[0])
            if adjective == None:
                if tup[1] in Sentence.__adjective_candidates:
                    adjective = tup[0]
        return Sentence.Crux(subject, predicate, None, adjective)
            

    # type 4: subject-verb-adverb
    def __independent_clause_4(self, tuples):
        subject = None
        predicate = []
        adverb = None
        
        for tup in tuples:
            if subject == None:
                if tup[1] in Sentence.__subject_candidates:
                    subject = tup[0]
            if tup[1] in Sentence.__predicate_candidates:
                predicate.append(tup[0])
            if adverb == None:
                if tup[1] in Sentence.__adverb_candidates:
                    adverb = tup[0]
        return Sentence.Crux(subject, predicate, None, adverb)
    
    # type 5: subject-verb-noun
    def __independent_clause_5(self, tuples):
        subject = None
        predicate = []
        noun = None
        
        for tup in tuples:
            if subject != None and noun == None:
                # a noun shouldn't be a personal pronoun
                if tup[1] in ["NN", "NNS", "NNP", "NNPS"]:
                    noun = tup[0]
            if subject == None:
                if tup[1] in Sentence.__subject_candidates:
                    subject = tup[0]
            if tup[1] in Sentence.__predicate_candidates:
                predicate.append(tup[0])
        return Sentence.Crux(subject, predicate, noun)
    
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
    def __split_sentence(self, tuples):
        return tuples
    
    
    # this is a prototype just to show how I imagined the sentence evaluation. the method probably belongs in the page_processor
    def __evaluate(self):
        # this is where our customization comes into play
        protected_actor_list = []
        protected_action_list = []
        # a bonus in case we want interactions with a specific actor to be censored in all cases
        shit_list = []

        tuples = nltk.pos_tag(nltk.word_tokenize(self.txt))
        max_value = -1 
        winning_crux = None
        for clause_parser in [self.__independent_clause_1, self.__independent_clause_5, self.__independent_clause_2, self.__independent_clause_3, self.__independent_clause_4]:
            crux = clause_parser(tuples)
            if crux.value() > max_value:
                winning_crux = crux
                max_value = winning_crux.value()
        self.crux = winning_crux
        return

        clauses = self.__split_sentence(tuples)
        
        aspects = []
        for clause in clauses:
            max_value = -1 
            winning_crux = None
            for clause_parser in [self.__independent_clause_1, self.__independent_clause_2, self.__independent_clause_3, self.__independent_clause_4, self.__independent_clause_5]:
                crux = clause_parser(clause)
                if crux.value() > max_value: winning_crux = crux
            aspects.append(winning_crux)
        
        censoring = False
        for aspect in aspects:
            if aspect.actor in protected_actor_list:
                if aspect.action in protected_action_list:
                    censoring = True
                if aspect.target in shit_list or aspect.modifier in shit_list:
                    censoring = True
        
        return censoring
        

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


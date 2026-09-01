#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
""" 
 
import string
 
def simple_lemmatize(word: str) -> str:
    """A very simple lemmatizer"""
    if not isinstance(word, str) or not word.strip():
        return ""

    word = word.lower().strip() 
    # Very basic rules
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"   
    elif word.endswith("ing") and len(word) > 4:
        return word[:-3]       
    elif word.endswith("ed") and len(word) > 3:
        return word[:-2]       
    elif word.endswith("s") and len(word) > 2:
        return word[:-1]      
    return word

def vector_norm(vec): 
    """ a vector normaization """
    if not isinstance(vec, (list, tuple)) or not vec:
        raise ValueError("Input must be a non-empty list or tuple of numbers.")
    
    total = 0.0
    for val in vec:
        if not isinstance(val, (int, float)):
            raise ValueError("All elements must be integers or floats.")
        total += val * val   
     
    return total ** 0.5

    
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def dot(vec1, vec2): 
    return  sum(i * j for i, j in zip(vec1, vec2))

def cosine_similarity(vector1, vector2):

    if len(vector1) == 0 or len(vector2) == 0:
        return 0.0
    
    dot_product = dot(vector1, vector2)
    norm_vector1 = vector_norm(vector1)
    norm_vector2 = vector_norm(vector2)
    if norm_vector1 == 0 or norm_vector2 == 0:
        return 0.0 
    similarity = dot_product / (norm_vector1 * norm_vector2) 
    return similarity

class TFIDF: 
    def __init__(self):
        self.weighted = False
        self.documents   = []
        self.corpus_dict = {} 
        self.b_fit = 0


    def add(self, description, key):
        """
          building a dictionary
        """
         
        doc_dict = {}
        for w in description:

            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
 
            if w in self.corpus_dict: 
               wid, wcnt = self.corpus_dict[w] 

               self.corpus_dict[w] =[wid, wcnt +  1]
            else:
               self.corpus_dict[w] = [len(self.corpus_dict), 1]
         
        length = float(len(description))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([key, doc_dict]) 
 
    def fit(self):
        return None
        if  self.b_fit == 1:
            imax = max(list (self.corpus_dict.values()))
            self.corpus_dict_norm = {}
            for k , v in self.corpus_dict.items():
                self.corpus_dict_norm[k] = v / float(imax)
            self.corpus_dict =  self.corpus_dict_norm
        self.b_fit = 1


       
    def edit_distance(self, word1, word2): 
       
       if not isinstance(word1, str) or not isinstance(word2, str):
           raise TypeError("Both inputs must be strings.")
    
       len1, len2 = len(word1), len(word2)
    
       # Create a DP matrix of size (len1+1) x (len2+1)
       dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
       # Initialize base cases
       for i in range(len1 + 1):
           dp[i][0] = i  # deletions
       for j in range(len2 + 1):
           dp[0][j] = j  # insertions
    
       # Fill the DP matrix
       for i in range(1, len1 + 1):
           for j in range(1, len2 + 1):
               if word1[i - 1] == word2[j - 1]:
                   cost = 0  # characters match
               else:
                   cost = 1  # substitution cost
    
               dp[i][j] = min(
                   dp[i - 1][j] + 1,      # deletion
                   dp[i][j - 1] + 1,      # insertion
                   dp[i - 1][j - 1] + cost  # substitution
               )
    
       return dp[len1][len2]

    def defition(self, word):
        return word
    
    def lemmatise(self, word):

        word = word.lower().strip()

        if word in self.corpus_dict: 
            return word
        
        _word = simple_lemmatize(word)
        if _word in self.corpus_dict: 
            return _word
        
        min_dist = 100
        closest_match = None
        for corp, v in self.corpus_dict.items():
            dist = self.edit_distance(word, corp) 
            if dist < min_dist:
                min_dist = dist
                closest_match = corp

            if dist < 1:
                return corp   
        return closest_match
    
    def similarities(self, list_of_words, imax = 3):
        """
        
        Returns a list of all the [docname, similarity_score] pairs relative to a list of words.
        
        """
        self.fit()
 
 
        # building the query dictionary
        query_dict = {}
        query_dict_norm = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict_norm[k] = query_dict[k] / length

        # computing the list of similarities
        sims = [] 
        def get_val(wrd):
            if wrd in self.corpus_dict:
                return self.corpus_dict[wrd][0]
            else:
                return 0.0

        for doc in self.documents:
            b_cat = False
            score  = 0.0 
            cnt    = 0.0
            doc_dict = doc[1]
            vec1 = [get_val(k) for k in doc_dict.keys()]
            vec2 = [get_val(k ) for k in query_dict.keys()]
            q_tot  = sum(vec2)
            if "snow" in doc_dict.keys():
                b_cat = True  

            for k in query_dict_norm:  
                if k in doc_dict:   
                    score += (query_dict[k] / self.corpus_dict[k][1]) + (doc_dict[k] / self.corpus_dict[k][1]) 
                    cnt += 1 
                 #   print(k, score, self.corpus_dict[k]  , query_dict[k], doc_dict[k])
                     
            imax = len(vec2)
            if len(vec1) > len(vec2):
                imax = len(vec1) 

            csim =  cosine_similarity(vec1[:imax], vec2[:imax])  
            if type(doc[0]) is dict: 
                sims.append([" ".join(list(doc_dict.keys())),   doc[0] ,   score]) 
            else:
                sims.append([" ".join(list(doc_dict.keys())),  " ".join(doc[0]) ,   score]) 
 
            #if  b_cat:
             #   print(csim, vec1, vec2,   " ".join(doc[0]) ," ".join(list(doc_dict.keys())))
              
         #   sims.append([doc[0], score]) 

        sims = sorted(sims, key=lambda x: x[2], reverse=True)[:imax]
       # sims = sorted(sims, key=lambda x: x[1], reverse=True)[:3] 
  
        return sims

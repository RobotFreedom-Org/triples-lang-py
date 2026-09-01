
import json 

try:
    from utils.utils import dispatcher  ,replace_sep, split_ignoring_quotes 
except:
    from triples.utils.utils import dispatcher  ,replace_sep, split_ignoring_quotes 

class Router():

    def __init__(self, docs, functions, root, kb):

        self.root = root
        self.memory = {}
        self.memory["functions_router"]= {} 
        self.kb = kb
        self.docs            = docs
        self.functions      = functions 
        self.function_lkup  =  functions
  
        try:
            self.load_functions_router()
             
        except:  
            self.build_functions_router()
            self.load_functions_router() 
    
    def build_functions_router(self):
     
        for convo_init_file  in [self.root +  "docs/router/semantic_functions_router.base.json" ,
                                 self.root +  "docs/router/semantic_functions_router.json"]: 
                
           for line in open(convo_init_file):
               row = json.loads(line.strip()) 
               self.kb.search_tfidf.add(row["prompt"].split(" ")  ,row  ) 
                
     
     
        res = [[k, {"prompt": v["function"]["example"].replace(";", " "), "function": k, "scores": 0.92}     ] for k ,v in  self.docs.items()]
        for row in res: 
              t = open("../trpls/" + row[0] + ".trpl", "w")
              cmd = row[1]["prompt"]
              t.write(cmd +"\n")

        self.kb.search_tfidf.add(row[0].split(" ")  ,row[1]  ) 

        res = [[k, {"prompt": v["function"]["examples"]["verbal"], "function": k, "scores": 0.92}  ] for k ,v in  self.docs.items() if "examples" in  v["function"] ]
        for row in res:
            self.kb.search_tfidf.add(row[0].split(" ")  ,row[1]    ) 

        self.kb.save(self.root +  "docs/router/"  + 'functions_router')
          
        
    def load_functions_router(self):  
        self.kb.load(self.root +  "docs/router/"  + 'functions_router') 

   
    def search(self, user_response, max_resp =5,  input_types =["prior_conversations", "defitions"]):
        """
        """   

        res = self.kb.search_tfidf.similarities(user_response) 
        return res 
       
    
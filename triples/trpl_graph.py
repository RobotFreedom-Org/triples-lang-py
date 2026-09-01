#!/usr/bin/python
# -*- coding: utf-8 -*- 
""" 
Author: RobotFreedom.org  
License: MIT License  
""" 
import json 
import uuid
import string 
 
from .lib.tfidf import TFIDF
from .lib.lemmatizer import simple_lemmatize

try:

    import nltk
    from nltk.stem import PorterStemmer 
    ps = PorterStemmer()

    def StemTokens(tokens):
        return [ps.stem(token) for token in tokens]  

    def StemNormalize(text, b_remove_stop = True):
        fin =  StemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
    
        if b_remove_stop:
            fin = [remove_stop(wrd) for wrd in fin]
    
        return fin
except:
    print("No NLTK found")

    def StemTokens(tokens):
        return [token for token in tokens]  

    def StemNormalize(text, b_remove_stop = True):
        fin =   text.lower().translate(remove_punct_dict).split(" ")
    
        if b_remove_stop:
            fin = [remove_stop(wrd) for wrd in fin]
    
        return fin
 

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def remove_stop(wrd):

    fin = wrd.replace(" the ", " ").replace(" of ", " ").replace(" a ", " ")
    if fin.startswith("the "):
        fin = fin[4:]
    if fin.startswith("a "):
        fin = fin[2:]
    if fin.startswith("of "):
        fin = fin[3:]
    if fin.endswith(" the"):
        fin = fin[:-4]
    if fin.endswith(" of"):
        fin = fin[:-3]
    if fin.endswith(" a"):
        fin = fin[:-2]
    return fin



class TrplGraph:

    def __init__(self,dbname="trpledb", remote=False):
        # Dictionary to store adjacency list
        """
        like an RDF graph
        
        """

        if remote:
            print("need to set up memcache")

        self.graph    = {}
        self.adj_list = {}
        self.adj_list["s_v"] = {}
        self.adj_list["v_s"] = {}
        self.adj_list["v_o"] = {}
        self.adj_list["o_v"] = {}
        self.adj_list["s_o"] = {}
        self.adj_list["o_s"] = {} 
        self.temporal = []


        self.search_tfidf = TFIDF()
 
        self.vert_data     = {} 
        self.triple_data   = {"name":dbname}

        self.v          = {} 
        self.r_v        = {} 
        self.e          = {} 
        self.links      = {}
        self.semantic_triples = None 


    def key_word_extractor(self :object, in_subjects :str = "", in_objects: str ="" )-> str:
        tops = {}  
        for wrd in in_subjects:
            src = 0
            if wrd in self.adj_list["v_o"]:
                scr +=.8
            if wrd in self.adj_list["o_s"]:
                scr +=1
            if wrd in self.adj_list["s_v"]:
                scr +=.5

            tops[wrd] = scr
        fin = sorted(tops,key=lambda x: x[1], reverse =True)
        fin = [v for v, s in fin is s > .01]
        return fin  


    def lemmatize(self: object, in_subjects :str = "", in_objects: str ="" )-> str:
         
        if in_objects == "":
            parts = ["v_o", "o_s", "s_v"]

        for part in parts:

            if in_subjects in self.adj_list[part]:
                return in_subjects
            
            _word = simple_lemmatize(in_subjects)
            if _word in self.adj_list[part]: 
                return _word
        
        return in_subjects
        

    def ret_svo(self, tripl_id):

        if tripl_id.find("->"):

            s_id, v_id, o_id  = tripl_id.split("->")

            return { "s":self.r_v[s_id],
                     "v":self.r_v[v_id],
                     "o":self.r_v[o_id]}
        else:
            return {"s":"", "v":"", "o":""}
 

    def update(self, s, v, o, time_stamp, prop={}): 
        """updates an temporal symantic between s.v and o."""

        linksv = []
        linkso = []

        if v in  self.adj_list:
            linksv = self.adj_list["v_o"][v]

        if s in  self.adj_list:
            linkso = self.adj_list["s_o"][s] 
            
        to_remove = []
        for link in linksv:
            if link in linkso:
                to_remove.append(link)

        for link in to_remove:
            #self.add_temporal(s, "prior " + v, link, time_stamp, prop)
            self.delete( v, link, "v_o")  

        self.add(s,v,o,prop)
 
    def build_temporal_graph(self,  time_start = -1, time_emd = 9999999999): 

        for s,v,o, prop, time in self.temporal:
            if time > time_start and time < time_emd:
                 triple_id = self.triple_id(s,v,o)
                 if triple_id in self.triple_data:
                     prop = self.triple_data[triple_id]
                     prop["temporal_cnt"] =   prop["temporal_cnt"] = 1
                     if "weight" in prop:
                         prop["temporal_weight"] = prop["weight"]
                 else:
                     prop["temporal_cnt"] = 1
                     if "weight" in prop:
                          prop["temporal_weight"] = prop["weight"]
                 self.add(s,v,o, prop )


 
    def add_temporal(self, s,v, o, time, prop): 

         if len(self.temporal) > 25:
             self.temporal = self.temporal[25:]
 
         self.temporal.append([s,v,o,prop, time]) 
  
    def delete(self,ent1,ent2, part): 
        #      self.adj_list[part][ent1].remove(ent2)
        del self.adj_list[part][ent1][ent2]

    def add(self, s, v, o, prop={}): 
        """Add s,v and o to symantic graph.""" 

        if s in self.r_v:
           s_id = self.r_v[s]  
        else: 
           s_id = self.get_id(s)
           s_prop = {"base_type":"subject", "id": s_id, "value":s}
           self.v[s_id] = s_prop 
           self.r_v[s]    = s_id
           self.r_v[s_id]    = s

        if v in self.r_v: 
           v_id = self.r_v[v]
        else:
           v_id = self.get_id(v)
           v_prop = {"base_type":"verb", "id": v_id , "value":v}
           self.v[v_id] = v_prop
           self.r_v[v]       = v_id
           self.r_v[v_id]    = v
        
        if o in self.r_v: 
           o_id = self.r_v[o]
        else:
           o_id = self.get_id(o)
           o_prop = {"base_type":"object",  "id" :o_id, "value":o }
           self.v[o_id] = o_prop 
           self.r_v[o]       = o_id
           self.r_v[o_id]    = o

        triple_id = self.triple_id( s_id,v_id,o_id )
        self.triple_data[ triple_id   ] = prop #"fact", qa, qq

        if "link_id" in prop:
            if triple_id not in self.e:
                self.e[triple_id] = [] 

            if prop["link_id"] not in self.e[triple_id]:
                self.e[triple_id].append(prop["link_id"])

            if prop["link_id"] not in self.e:
                self.e[prop["link_id"]] = [] 

            if triple_id not in self.e[prop["link_id"]]:
                self.e[prop["link_id"]].append(triple_id)

        self._add_to_adj( self.adj_list["s_v"], s_id,  v_id) 
        self._add_to_adj( self.adj_list["v_s"], v_id,  s_id)   

        self._add_to_adj( self.adj_list["v_o"], v_id,  o_id)
        self._add_to_adj( self.adj_list["o_v"], o_id,  v_id)

        self._add_to_adj( self.adj_list["s_o"], s_id,  o_id)
        self._add_to_adj( self.adj_list["o_s"], o_id,  s_id)  

    def _add_to_adj(self, adj, v1, v2):

        if v1 not in adj:
            adj[v1] = {} 
        adj[v1][v2] = 1 

        """  
        if v1 not in adj:
            adj[v1] = set([]) 
        adj[v1].add(v2) 
        """

    def get_id(self, val = None):
        if val:
            return val
        else:
            return  str(uuid.uuid4())
    
    def triple_id(self, s, v, o):
  
           return  s + "->" + v + "->" + o
    
    def triple_value(self, s, v, o):
    
        if s in self.v:
            s_prop = self.r_v[s] 
        else:
            return 'NA'
    
        if v in self.v:
            v_prop = self.r_v[v] 
        else:
            return 'NA'  
    
        if o in self.v:
            o_prop = self.r_v[o]  
        else:
            return 'NA'
    
        return  s_prop["id"] + "->" + v_prop["id"] + "->" + o_prop["id"]
    
    def load_trlps(self, folder_name, db, default_type="data"): 
        
        entities = {} 
        entities_file = open(folder_name + "/entity2id.txt") 
        for i, row in enumerate(entities_file):
            row = row.strip()
            if i > 0: 
              arow = row.split("\t") 
              if arow[0].find(".") > -1: 
                  _ent = arow[0].split(".")[0] 
                  ent =  " ".join(StemNormalize(_ent))  
                  entities[arow[1]] = ent

              elif len(arow) == 1: 
                  entities[""] = arow[0] 
              else:
                  _ent =  arow[0] 
                  ent =  " ".join(StemNormalize(_ent))
                  entities[arow[1]] = ent
    
        relationships = {} 
        relationships_file = open(folder_name + "/relation2id.txt")
        
        for i, row in enumerate(relationships_file):
            row = row.strip()
            if i > 0:
              arow = row.split("\t")
              if len(arow) == 1:

                  relationships[arow[0]] = "" 
              else:
                  _relate = arow[0]  
                  relate =  " ".join(StemNormalize(_relate, True) )
                  relationships[arow[1]] = relate 
    
        facts  = []
        links_file = open(folder_name + "/gt2id.txt")


        queries =  [] 
        questions = {}  
        try:
            questionss_file = open(folder_name + "/question2id.txt")
        except: 
            questionss_file = []
        
        for i, row in enumerate(questionss_file):
            row = row.strip()
            if i > 0:
              arow = row.split("\t")
              if len(arow) ==1:
                  questions[arow[0]] = "" 

              else:
                  _relate = arow[0] 
                  relate =  " ".join(StemNormalize(_relate))
                  questions[arow[1]] = relate  

        try:
             query_file = open(folder_name +"/query2id.txt")
        except: 
            query_file = []
        for line in query_file:
            queries.append(line.strip())
            

        for i, row in enumerate(links_file):

            row = row.strip() 
            if i > 0: 
              arow = row.split(" ")  
              
              ent1     = entities[arow[0]].lower() 
              ent2     = entities[arow[1]].lower() 
              verb     = relationships[arow[2]].lower()   
     
              link_id = None
    
              if len(queries) > i:
                  link_id = self.get_id()

                  arowq = queries[i].split(" ") 
                  ent1_q     =   entities[arowq[0]].lower() 
                  if ent1_q == "me":
                      ent1_q = "you"
                  ent2_q     = entities[arowq[1]].lower() 
                  verb_q     = questions[arowq[2]].lower()  
     
                  self.add(ent1_q, verb_q, ent2_q, {"link_id":link_id, "type":"q", "source":db} )
     
              if link_id is not None:
                 self.add(ent1, verb, ent2,{"link_id":link_id, "type":"a", "source":db} ) 

                 trp_id_1 = self.triple_id(ent1, verb, ent2)
                 trp_id_2 = self.triple_id(ent1_q, verb_q, ent2_q)
                 """ 
                 if link_id not in  self.links:
                       self.links[link_id] = {}
                 if link_id not in  self.links:
                       self.links[link_id] = {}

                 if trp_id_1 not in  self.links[link_id]:
                       self.links[link_id][trp_id_1] = [] 

                 if trp_id_2 not in  self.links[link_id]:
                       self.links[link_id][trp_id_1] =  []
                     
                 self.links[link_id][trp_id_1].append(trp_id_2) 
                 self.links[link_id][trp_id_2].append(trp_id_1) 
                 """

              else:   
                 self.add(ent1, verb, ent2, {"type":default_type, "source":db} )  
 

    def get_svo(self, s_id, v_id, o_id ): 

        s,v,o = "","",""

        if s_id in self.v:
            s = self.v[s_id]["value"]
        if v_id in self.v:
            v = self.v[v_id]["value"]
        if o_id in self.v:
            o = self.v[o_id]["value"]

        return {"s":s, "v":v, "o":o}
        
    def linked(self, s, v, o, priority={"type":"a"}, b_stop_on_found = False): 

        s_id = "na"
        v_id = "na"
        o_id = "na"
        if s in self.r_v:
            s_id = self.r_v[s]
        if v in self.r_v:
            v_id = self.r_v[v]
        if o in self.r_v:
            o_id = self.r_v[o]  

        trp_id = self.triple_id(s_id, v_id, o_id)

        if trp_id in self.e:
           links = self.e[trp_id]
           res =[]

           for lnk in links:  
              edges = self.e[lnk] 
              for edge in edges:
                 
                 linked  =  edge.split("->")

                 if linked[0] != s_id:  
                     res.append(self.get_svo(linked[0],linked[1],linked[2] )) 
    
           return res
        else:
            return []
 

    def triples(self, s,v,o):
        """
        swap with triples()
        """
 
        s_id = "na"
        v_id = "na"
        o_id = "na"
        if s in self.r_v:
            s_id = self.r_v[s]
        if v in self.r_v:
            v_id = self.r_v[v]
        if o in self.r_v:
            o_id = self.r_v[o]   

        trp_id = self.triple_id(s_id, v_id, o_id)
        if trp_id  in  self.triple_data :
            tp = self.triple_data[trp_id]    
            return {"s":s , "v": v, "o": o} #, tp["type"]]) 
        
        return {"s":"", "v":"", "o":""}

    def similar(self, s, v, o, priority={"type":"a"}, b_stop_on_found = False, create_new=False):
        """
        
        """
        potentials = []
        b_found = False
        s_id = ""
        v_id = ""
        o_id = ""

        if s in self.r_v:
            s_id = self.r_v[s].strip()
        if v in self.r_v:
            v_id = self.r_v[v].strip()
        if o in self.r_v:
            o_id = self.r_v[o].strip()  
 

        trp_id = self.triple_id(s_id, v_id, o_id)
        
        if trp_id  in  self.triple_data :
            tp = self.triple_data[trp_id] 
            if tp["type"] == priority["type"] :  
                  potentials.append([{"s":s , "v": v, "o": o}, 5, tp["type"]]) 
            else:
                  potentials.append([{"s":s , "v": v, "o": o}, 3, tp["type"]]) 
  
        rules = {}
        rules["s"]   = ["s", s, s_id, "v", v ,v_id, "o",o] 
        rules["v"]   = ["v", v, v_id, "o", o ,s_id, "s",s]
        rules["o"]   = ["o", o, o_id, "s", s ,s_id, "v",v]   
        rules["o1"]  = ["o", s, s_id, "v", v ,v_id, "s",o]    
        rules["s1"]  = ["s", o, o_id, "o", o, o_id, "v",v] 
        rules["o2"]  = ["o", o, s_id, "v", v ,v_id, "s",s]    
        rules["s2"]  = ["s", s, o_id, "o", o, o_id, "v",v]


        
 
        for s_type in ["s", "v", "o", "o1", "s1", "o2", "s2"]: 
               
               rule      = rules[s_type]

               start_t   = rule[0]
               start_id  = rule[1]
               start_v   = rule[2]

               next_t    = rule[3]
               next_id   = rule[4]
               next_v    = rule[5]

               missing_t = rule[6]
               missing_v = rule[7]
 
              
               if start_id not in  self.adj_list[start_t + "_" + next_t]  :  
                   continue 
               
               for pot_1_id in  self.adj_list[start_t + "_" + next_t][ start_id ] : 
                   
                   
                   pot_1_val = self.r_v[pot_1_id]  
                    
                   for pot_2_id in  self.adj_list[next_t + "_" + missing_t][ pot_1_id ]:

                     if start_id in self.adj_list[missing_t + "_" + start_t][pot_2_id]:
 
                         pot_2_val = self.r_v[pot_2_id]   


                         _res= {"s":"", "v":"", "o":""}
                         _res[start_t]   = start_v 
                         _res[next_t]    = pot_1_val
                         _res[missing_t] = pot_2_val

                         triple_id = self.triple_id(_res["s"],_res["v"],_res["o"])
                         if triple_id not in self.triple_data and create_new is False:
                             continue
                         
                         scr = 1
                         if pot_1_val in [next_v, missing_v]:
                             scr +=1
                         if pot_2_val in [next_v, missing_v]:
                             scr +=1
                         potentials.append([_res, 3, ""]) 
 

        if b_stop_on_found is False :
            b_found = False  

        potentials = [res for res in potentials if res[0]["s"] != "" and res[0]["v"] != "" and  res[0]["o"] != "" ]
        potentials = sorted(potentials, key = lambda x: x[1], reverse=True) 
        return potentials      
    
    def related(self, s, v, o,  return_data = False):
        """
        
        """
        potentials = []
        b_found = False
        s_id = ""
        v_id = ""
        o_id = ""

        if s in self.r_v:
            s_id = self.r_v[s].strip()
        if v in self.r_v:
            v_id = self.r_v[v].strip()
        if o in self.r_v:
            o_id = self.r_v[o].strip()  
 

        trp_id = self.triple_id(s_id, v_id, o_id)
        
        if trp_id  in  self.triple_data :
            tp = self.triple_data[trp_id] 
            potentials.append([{"s":s , "v": v, "o": o}, 3, tp["type"]]) 
  
        rules = {}
        rules["s"]   = ["s", s, s_id, "v", v ,v_id, "o",o] 
        rules["v"]   = ["v", v, v_id, "o", o ,s_id, "s",s]
        rules["o"]   = ["o", o, o_id, "s", s ,s_id, "v",v]   
        rules["o1"]  = ["o", s, s_id, "v", v ,v_id, "s",o]    
        rules["s1"]  = ["s", o, o_id, "o", o, o_id, "v",v] 
        rules["o2"]  = ["o", o, s_id, "v", v ,v_id, "s",s]    
        rules["s2"]  = ["s", s, o_id, "o", o, o_id, "v",v]
 
 
        for s_type in ["s", "v", "o", "o1", "s1", "o2", "s2"]: 
               
               rule      = rules[s_type]

               start_t   = rule[0]
               start_id  = rule[1]
               start_v   = rule[2]

               next_t    = rule[3]
               next_id   = rule[4]
               next_v    = rule[5]

               missing_t = rule[6]
               missing_v = rule[7]
 
              
               if next_id == "":
                      continue
               
               if start_id not in  self.adj_list[start_t + "_" + next_t]  :  
                   continue 
               
               for pot_1_id in  self.adj_list[start_t + "_" + next_t][ start_id ] : 

                
                   if next_id != pot_1_id:
                       continue
                   
                   pot_1_val = self.r_v[pot_1_id]  
                    
                   for pot_2_id in  self.adj_list[next_t + "_" + missing_t][ pot_1_id ]:

                     if start_id in self.adj_list[missing_t + "_" + start_t][pot_2_id]:
 
                         pot_2_val = self.r_v[pot_2_id]   
 
                         _res= {"s":"", "v":"", "o":""  }
                         _res[start_t]   = start_v 
                         _res[next_t]    = pot_1_val
                         _res[missing_t] = pot_2_val

                         triple_id = self.triple_id(_res["s"],_res["v"],_res["o"])
                         if triple_id not in self.triple_data:
                             continue
                         _res["data"] = self.triple_data[triple_id] 

                         scr = 1
                         if pot_1_val in [next_v, missing_v]:
                             scr +=1
                         if pot_2_val in [next_v, missing_v]:
                             scr +=1
                         potentials.append([_res, 3, ""] ) 
  
        potentials = [res for res in potentials if res[0]["s"] != "" and res[0]["v"] != "" and  res[0]["o"] != "" ]
        potentials = sorted(potentials, key = lambda x: x[1], reverse=True) 
        return potentials     

    def copy(self, trpl_grpah): # type: ignore
         import copy
         self.adj_list    = copy.deepcopy(trpl_grpah.adj_list)
         self.vert_data   = copy.deepcopy(trpl_grpah.vert_data  )
         self.triple_data = copy.deepcopy(trpl_grpah.triple_data)
         self.links       = copy.deepcopy(trpl_grpah.links )
         self.v           = copy.deepcopy(trpl_grpah.v)
         self.r_v         = copy.deepcopy(trpl_grpah.r_v)
         self.e           = copy.deepcopy(trpl_grpah.e   )   
         self.search_tfidf.corpus_dict     = copy.deepcopy(trpl_grpah.search_tfidf.corpus_dict)
         self.search_tfidf.documents       = copy.deepcopy(trpl_grpah.search_tfidf.documents)

    def load(self, graph_name ="robot_freedom"):
         
         t_in = open(graph_name + ".trlgrp")
         s_json = ""
         for line in t_in:
             s_json += line
         grph = json.loads(s_json ) 
         self.adj_list    =  grph["adj_list"]  
         self.vert_data   = grph["vert_data"] 
         self.triple_data = grph["triple_data"]  
         self.links       = grph["links"]     
         self.v     = grph["v"]  
         self.r_v   = grph["r_v"]    
         self.e     = grph["e"]      
         self.search_tfidf.corpus_dict     = grph["corpus_dict"]    
         self.search_tfidf.documents       = grph["documents"]    

    def save(self, graph_name = "robot_freedom"):
         t_out = open(graph_name + ".trlgrp", "w")
         grph = {}
         grph["adj_list"]    = self.adj_list 
         grph["vert_data"]   = self.vert_data
         grph["triple_data"] = self.triple_data
         grph["links"]       = self.links
         grph["v"] = self.v
         grph["r_v"] = self.r_v
         grph["e"] = self.e 
         grph["corpus_dict"] =   self.search_tfidf.corpus_dict      
         grph["documents"]   =   self.search_tfidf.documents   
         t_out.write(json.dumps(grph))

    def edges(self, v, data=False):

        if data:
           fin = []
           return self.adj_list[v]

        else:
           return self.adj_list[v]

    def has_edge(self, u, v):
        """Check if an edge exists between u and v."""
        return v in self.adj_list.get(u, set())

    def adjacency(self):
        return self.adj_list
    
    def infer_edges(self, query_type = "s_v"):
        """
        Infer possible edges based on transitive connections.
        Example: If A-B and B-C exist, suggest A-C.
        """ 
        inferred = set()

        for s in  self.adj_list["s_v"].keys(): 
           for v in  self.adj_list["s_v"][s]:    
                for o  in  self.adj_list["v_o"][v]:  
                   for v2  in  self.adj_list["o_v"][o]:   
                       if v != v2:
                           inferred.add(v2)   
                   for s2  in  self.adj_list["o_s"][o]:   
                       if s != s2:
                           inferred.add(v2)   
        return inferred

    def __str__(self):
        return "\n".join(f"{node}: {sorted(neigh)}" for node, neigh in self.adj_list.items())

if __name__ == '__main__': 
     """
     
     """
     trpl_graph = TrplGraph()

    # trpl_graph.load("../../responses_to_questions")
    # trpl_graph.load("../../revist_graph")

     trpl_graph.load_trlps("../../data/chat/personal/", "personal") 
     trpl_graph.load_trlps("../../data/knowledge/THOR_U/",   "common_sense") 

     id = trpl_graph.get_id() 
     trpl_graph.add("you", "how", "feel", {"type":"q", "link_id": id})
     trpl_graph.add("me", "feel", "good", {"type":"a", "link_id": id}) 

     id = trpl_graph.get_id()
     trpl_graph.add("you", "what", "name",   {"type":"q", "link_id": id}) 
     trpl_graph.add("me", "name", "number 3", {"type":"a", "link_id": id}) 

     #trpl_graph.load_trlps("../../data/chat/convo", "convo") 
     # trpl_graph.load_trlps("../../data/chat/facts", "facts") 

     res = trpl_graph.triples("you", "how", "feel", {"type":"a"})  
     print(res)

     res = trpl_graph.triples("you", "", "feel", {"type":"a"})  
     print(res)

     res = trpl_graph.triples("", "how", "feel", {"type":"a"})  
     print(res)

     res = trpl_graph.triples("you", "", "feel", {"type":"a"})  
     print(res)


     #inf = trpl_graph.infer_edges()
     #print(inf)
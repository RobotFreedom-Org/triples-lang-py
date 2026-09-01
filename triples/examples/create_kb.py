
import json
 

STOPWORDS= [" a ", " the "]
 

def gen_kg(kb ,   file_path):

    inputs = []
    responses = []
    with open(file_path, 'r') as in_data:   
        for line in in_data: 
            row = json.loads(line.lower().strip())     
            tokens = [wrd for wrd in row["completion"].split(" ") if wrd not in STOPWORDS]  
            kb.search_tfidf.add(row["prompt"], tokens)  
    return True 


if __name__ == '__main__': 
     """
     
     """ 
 

     import os, sys
     print("source ~/venv_rf/bin/activate")
     os.chdir('../')
     sys.path.insert(0, os.path.abspath('./')) 

     from triples.trpl_graph import TrplGraph 
     import config   
     trpl_graph = TrplGraph() 
     gen_kg(trpl_graph, config.CHAT_PATH + "facts/simple_dictionary.json" ) 

     id = trpl_graph.get_id()
     trpl_graph.add("you", "what", "name",   {"type":"q", "link_id": id}) 
     trpl_graph.add("me", "name", "number 3", {"type":"a", "link_id": id}) 

     #trpl_graph.load_trlps("../../data/chat/convo", "convo") 
     # trpl_graph.load_trlps("../../data/chat/facts", "facts") 

     # first prcoess all words and find most similar using edit distance 

     res = trpl_graph.search_tfidf.similarities("school".split(" "))
     print(res)  
      
     res = trpl_graph.search_tfidf.similarities("to form words with a pen or pencil".split(" "))
     print(res)   
    
     res = trpl_graph.search_tfidf.similarities("legs".split(" "))
     print(res)  

     query = [trpl_graph.search_tfidf.lemmatise(w) for w in "to frm word with a pen or pensil".split(" ")]
     print(query)
     res = trpl_graph.search_tfidf.similarities(query)
     print(res)   
          
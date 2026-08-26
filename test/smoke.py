import unittest
import os, sys
os.chdir('../')
sys.path.insert(0, os.path.abspath('./'))   
from triples.core import Triples
triples = Triples() 
 
class TestMathOperations(unittest.TestCase):
     
     def test_addition(self): 
        res = triples.add("v1", "v2")
        self.assertEqual(res, 5)

     def test_addition_cd(self): 
        res = triples.run("add v1 v2;")
        self.assertEqual(res, 5)

     def test_subtract(self): 
        res = triples.subtract("v1", "v2")
        self.assertEqual(res, -1)

     def test_subtract_cd(self): 
        res = triples.run("subtract v1 v2;")
        self.assertEqual(res, -1)


class TestStringOperations(unittest.TestCase):
     
     def test_join(self): 
        res = triples.join("v3", "v4")
        self.assertEqual(res, "hello world")

     def test_join_cd(self): 
        res = triples.run("join v3 v4;")
        self.assertEqual(res, "hello world")       

     def test_upper(self): 
        res = triples.upper("v3" )
        self.assertEqual(res, "HELLO")

     def test_upper_cd(self): 
        res = triples.run("upper v3;")
        self.assertEqual(res, "HELLO") 

     def test_lower(self): 
        res = triples.lower("v5" )
        self.assertEqual(res, "test")

     def test_lower_cd(self): 
        res = triples.run("lower v5;")
        self.assertEqual(res, "test") 

     def test_replace(self): 
        res = triples.replace("v3", "h->g" )
        self.assertEqual(res, "gello")

     def test_replace_cd(self): 
        res = triples.run("replace v3 h whither g;")
        self.assertEqual(res, "gello") 

class TestLogicOperations(unittest.TestCase):
     
     def test_less(self): 
        res = triples.less("v1", "v2")
        self.assertEqual(res, 1)

     def test_less_cd(self): 
        res = triples.run("less v1 v2;")
        self.assertEqual(res, 1)       
 
     def test_more(self): 
        res = triples.more("v1", "v2")
        self.assertEqual(res, 0)

     def test_more_cd(self): 
        res = triples.run("more v1 v2;")
        self.assertEqual(res, 0)     
     
     def test_different(self): 
        res = triples.different("v1", "v2")
        self.assertEqual(res, 1)
     
     def test_different_cd(self): 
        res = triples.run("different v1 v2;")
        self.assertEqual(res, 1)     

class TestFlow(unittest.TestCase):
     
     def test_if_1(self): 
         triples.flow("if", "start") 
         triples.less("v1", "v2")
         triples.echo('conditional 1') 
         res = triples.flow("if","end")
         self.assertEqual(res, ["conditional 1"])

     def test_if_1_cd(self): 
        res = triples.run(["flow if start;",
                            "less v1 v2;",
                            'echo "conditional 1" out;',
                            "flow if end;",
                           ])
        self.assertEqual(res, ["conditional 1"])       

if __name__ == "__main__":
    """

    """

    triples.set("v1",2)
    triples.set("v2",3)

    triples.set("v3","hello")
    triples.set("v4","world")
    triples.set("v5","TEST")

    unittest.main()  
                
    """  
    triples.flow("if", "start") 
    triples.less("v5", "v6")
    triples.echo("conditional 2") 
    res = triples.flow("if","end") 
    print(res) 
    
    triples.create("function", "myfunct")  
    triples.set("var1",1) 
    triples.set("var2",2) 
    triples.add("var1","var2") 
    triples.echo("Function ran")  
    triples.create("function", "end") 

    res = triples.echo("created function")  
    print(res)
    print(triples.execute("myfunct") )
 
    res = triples.time() 
    print(res)  
    triples.file("read", "quick_start.sh")  
    triples.echo("row")  
    triples.file("close")    

    triples.set("v7" , 0)
    triples.set("v8" , 1)
    triples.flow("while", "start")     
    triples.increment("v7"  ) 
    triples.flow("if", "start") 
    triples.more("v7", "v8")
    triples.flow("break")
    triples.flow("if","end") 
    triples.echo("v7", "shell")
    triples.temporal("pause", 1)
    res = triples.flow("while", "end")  

    print(res)  
    """
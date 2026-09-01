# <img src="./robot_freedom_ai/assets/logo_small.png" width="40">  Triples-Lang 

Welcome to the official robotic langauage call Triples maintained by RobotFreedom.org. This code is designed to help students of all ages get hands on experience with AgenticAI platforms.  

Triples is a software language designed for AgenticAI Agents to use and create their own tools, integrated with a RDF database and communicate with other AIs.

The language is designed for portablity and has a Python and CPP engines.

Triples-Lang is focused on interacting with Resource Description Framework (RDF) databases and the syntax follows a subject, verb, object (SVO) paradigm as much as possible. The SVO paradigm was chosen because it links directly to a RDF database meaning the returns for queries can be directly executed. Also LLMs are well suited parsing natural text to SVO and a non-LLM parser can be easily developed for deployment environments where LLMs are not an option like an Arduino. 

Triples-Lang is an explicit language reducing potential confusion and enabling it to be read out loud for interfacing verbally with a AgenticAI agent like a robot. However, its primary motivation is for an AI – not a human – to naturally connect to a RDF database.

## Table of Contents 

- [What's New](#what-is-new)
- [Installation](#installation)  
- [Getting Started](#getting-started)  
- [Examples](#examples)
- [Operators](#operators)
- [Basic Commands](#basic-commands)

## What's New

This is the first alpha release, and there is still a lot of work to be done. 
 



## Installation

First, download this repro and unzip it on your Desktop or projects folder. Then, open a terminal and navigate to Triples-Lang.

Note: We prefer to not install Triples-Lang as a package because this project is primarily a teaching tool not production code. We want people to experiment and change the code on demand and package installations make this difficult.  

The setup is slight different depending on whether you are using OSX, Windows or Linux. The code will run on degraded mode on most platforms but will only be fully functional on a RaspberryPi. 

First, if you do not have Python3 and Pip installed please do before you begin.

Triples-Lang does not have any exteranal requirements to ease deployment.


## Getting Started

Triples-Lang is designed as a secure language for AI agents and not inteneded to compete other languages like Java, Python or C++. 

To run a Triples-Lang script use the -f parameter when calling triples-lang.py

```bash 
python3 triples-lang.py ../examples/add.trpl
```   

You can also enter interactive mode by  running triples-lang.py without a pass parameter

```bash 
python3 triples-lang.py 
```    

Help provides a list of avaible functions.

```bash 
> help; 
```

__NOTE__

For the Python and CPP engine commands may or may not terminate with a ";" but for the Arduino engine all commands must end with a ";".

You can also import Triples-Lang into a Python program and use it directly.

```bash 
from triples.core import Triples 
triples = Triples()  
    
code = "routine create params\n"   
code += 'echo "hello world"\n'  
code += "routine create end\n"    
code += "routine execute params\n"    
res = triples.run(code.split("\n"))
print( res) 

```


## Testing

All the tests directly use the libraries for clarity. Each example assumes you are starting in the root directory of the project.

```bash
cd ./triples-lang/triples/test 
python smoke.py
```    

## Examples

Creating a variable uses the set command.

```bash 
set myar 1
```

You can retrieve a variable using the get or echo commands.

```bash 
echo myvar
```

Logic commands return a 1 or 0 (True /False). A number is return to make the output more portiable to Arduinos. 

```bash 
set myvar2 3
more myvar1 myvar2
```

Math functions return numeric (float) values

```bash 
add myvar1 myvar2
```

Flow control is define between a start and end. After the end statement to cocde block is executed unless the block is inside another block.

```bash  
flow if start 
less myvar1 myvar2 
echo hello 
flow if end 
```

While statements are also define by a beginning and end statement. Make sure to define a exit condition our the code will run continuiously. While block are often used to monitor sensor readings.

```bash 
set v1 0;
set v2 3;
flow while start;
increment v1;
flow if start;
more v1 v2;
flow break;
flow if end;
temporal pause one; 
echo v1; 
flow while end;
```

File are processed once file is closed.

```bash 
file read README.md
echo row;
file close;
```

User routines are run using the execute parameter. 

```bash 
routine create myfunction;
echo "hello world";
routine create end;

routine execute myfunction;
```

You can set a varible to the output of a functions using the whense operator.

```bash  
set v3 whence roll 10d; 
echo v3;
set v4 whence join "i just rolled a " v3  ;
echo v4; 
```

## Operators

Triples-Lang does not have operators in a tradtional sinse becuase it is met to be spoken., Instead it maps seldom used early Modern English words to operators.

Put next output into prior statment (<-) 

```bash 
whense
```

Put prior ouput into next statment (->)
```bash 
whither
``` 
  

Comments are denoted by starting the line with the word annoatation 
```bash 
annotation
```

Other standard operators like + and - are called as functions add and subtract.

  

## Basic Commands
 
__VARIABLES__

*set* 

Stores a numeric value to memory

```bash 
set myvar 1
```

*set* 

Stores a string value to memory

```bash 
set mytextvar  "hello world"
```

*get*

Retrieve a variable from memeory

```bash 
get myvar
```


__MATH__

*add*

Adds two variables together

```bash  
add myvar1 myvar2
```

*subract*

Subtracts two variables together

```bash  
subtract myvar1 myvar2
```

*divide*

Divides two variables together

```bash  
divide myvar1 myvar2
```

*multiple*

Multiples two variables together

```bash  
multiple myvar1 myvar2
```

*decrement*

Decreases the value of a variables  

```bash  
decrement myvar1 1
```

*increment*

Increases the value of a variables  

```bash  
increment myvar1 1
```

__STRING__

*lower*

Lowercaes a strings 

```bash  
lower mytextvar1
```

*upper*

Uppercaes a strings 

```bash  
upper mytextvar1
```

*split*

Splits a strings 

```bash  
split mytextvar1 ,
```

*replace*

Replace a character or characters with a passes character or characters in a strings 

```bash  
replace mytextvar1 dog whither cat
```


*join*

Adds to strings together

```bash  
join mytextvar1 mytextvar2
```

__LOGIC__

*more*

Returns 1/0 based on is the first varible is more than the second.

```bash  
more myvar1 myvar2
```

*less*

Returns 1/0 based on is the first varible is less than the second.

```bash  
less myvar1 myvar2
```
 
*different*

Returns 1/0 based on is the first varible is different than the second.

```bash  
different myvar1 myvar2
```

*equal*

Returns 1/0 based on is the first varible is equal than the second.

```bash  
equal myvar1 myvar2
```

__INPUT/OUTPUT__

*echo*

Returns a value to command stream.


```bash  
echo "hello world"
```

*echo*

If a file name is specifed will write ouput to a file.

```bash  
echo "hello world" "myfile.out"
```

*file*

Reada a file  

```bash  
file read README.md
echo row;
file close;
```
 
__CONDITIONAL__

*flow if*
 
Define a conditional using the flow if command.

```bash  
flow if start
more myvar1 myvar2
echo "condition met"
flow if end
```

__FLOW CONTROL__

*flow while*
 
Define a while statement using the flow command.

```bash  
flow if start
more myvar1 myvar2
echo "condition met"
flow if end
```


__ROUTINES__

*routine*

Define routines using the create directive.

```bash  
routine create my_funct 
echo "Hello world!"
routine create  end
```

*execute*

Run a routine using the execute directive.

```bash  
routine execute my_funct  
```

*create pass parameters*

Unlike other languages pass parameters are handled by create global values.

```bash  
set param1 1 
set param2 2  
routine create params 
add param1 param2  
routine create end    
routine execute params   
'''
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k',
                 streaming=True,
                 callbacks=[StreamingStdOutCallbackHandler()],
                 temperature=0
                 )

prompt = """System: You are a product manager, and your job is to design software. You are provided a rough 
description of the software. Expand on this description and generate the complete set of functionalities needed to 
get that software to work. Don't hesitate to make design choices if the initial description doesn't provide enough 
information. Don't generate code or unit tests!!

Human: {input}

Complete software design:
"""

product_manager_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)


prompt = """System: You are a Software engineering technical lead writing code in Python. Your job is to come up with 
a detailed description of all the necessary functions, classes, methods, unit tests for the code and attributes for 
the following software description. Make sure to design a software that incorporates all the best practices of 
software development. Make sure you describe how all the different classes and function interact between each other. 
The resulting software should be a fully functional. Produce Mermaid class and sequence 
diagrams also as an output. Don't generate code or unit tests!!

Software description: 
{input}

Software design:
"""

tech_lead_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """System: You are a Software Testing Engineer and your job is to design test plans for software. Provide a 
detailed test plan and test cases to test the following software. Make sure to design a test plan that incorporates 
all the best practices of software testing.

Software description: 
{input}

Software test plan:

"""

test_lead_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """
System: You are a Software Engineer and your job is to design software in Python. 
Provide a detailed description of the file structure with the required folders and Python files.
Make sure to design a file structure that incorporates all the best practices of software development.
Make sure you explain in which folder each file belong to.
Folder and file names should not contain any white spaces. 
A human should be able to exactly recreate that file structure.
Make sure that those files account for the design of the software
Don't generate non-python files.

Software design: {input}

File structure:
"""

file_structure_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)


prompt = """System: Return the complete list of the file paths, including the folder structure using the following 
list of python files. Only return well formed file paths: ./<FOLDER_NAME>/<FILE_NAME>.py

Follow the following template:
<FILE_PATH 1>
<FILE_PATH 2>
...

Human: {input}

File paths list:
"""

file_path_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)


prompt = """System: You are a Software Engineer. Your job is to write python code. Write the code for the following 
file using the following description. Only return code! The code should be able to run in a python interpreter. Make 
sure to implement all the methods and functions. Make sure to import all the necessary packages. The code should be 
complete.

Files structure: {structure}

Software description: {class_structure}

File name: {file}

Python Code for this file:
"""

code_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)


prompt = """
Return `<TRUE>` If the following Python code contains non-implemented parts and return `<FALSE>` otherwise

If a python code contains `TODO` or `pass`, it means the code is not implemented.

code: {code}

Return `<TRUE>` if the code is not implemented and return `<FALSE>` otherwise:
"""

missing_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """System: You are a Software Engineer. The following Python code may contain non-implemented functions. If 
the code contains non-implemented functions, describe what additional functions or classes you would need to 
implement those missing implementations. Provide a detailed description of those additional classes or functions 
that you need to implement. Make sure to design a software that incorporates all the best practices of software 
development.

Class description: {class_structure}

Code: {code}

Only return text if some functions are not implemented.
The new classes and functions needed:
"""

new_classes_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)
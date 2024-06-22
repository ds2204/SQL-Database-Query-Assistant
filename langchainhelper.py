from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.llms import GooglePalm
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate

def get_few_shot_db_chain():

 db_user = "dp"
 db_password = "1234"
 db_host = "LAPTOP-2I2RORCB\\MSSQLSERVER01"
 db_name = "mob"

 # Construct the connection string
 connection_string = (
    f"mssql+pyodbc://{db_user}:{db_password}@{db_host}/{db_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
 )

 # Create the SQLDatabase instance
 db = SQLDatabase.from_uri(connection_string, sample_rows_in_table_info=3)
 api_key='AIzaSyBMsodDM83vnKaN-EmUps1ekWKm1nAp3vA'
 llm=GooglePalm(google_api_key=api_key,temperature=0.5)
 few_shots = [
    {
        'Question': "How many Apple mobiles do we have left for model1 in white color?",
        'SQLQuery': "SELECT stock_quantity FROM mobiles WHERE brand = 'Apple' AND model = 'Model 4' AND color = 'White';",
        'SQLResult': "Result of the SQL query",
        'Answer': "71"
    },
    {
        'Question': "How many Samsung phones do we have in stock of all models?",
        'SQLQuery': "SELECT SUM(stock_quantity) FROM mobiles WHERE brand = 'Samsung';",
        'SQLResult': "Result of the SQL query",
        'Answer': "1183"
    },
    {
        'Question': "Do you have the Sony Xperia 1 II in stock?",
        'SQLQuery': "SELECT COUNT(*) FROM mobiles WHERE model = 'Sony Xperia 1 II';",
        'SQLResult': "Result of the SQL query",
        'Answer': "No"
    },
    {
        'Question': "Can you check if the Google model 1 is available in gold?",
        'SQLQuery': "SELECT color FROM mobiles WHERE model = 'Model 1' AND brand = 'Google' AND color = 'Gold';",
        'SQLResult': "Result of the SQL query",
        'Answer': "Yes"
    },
    {
        'Question': "Are there any eco-friendly or sustainable phone options?",
        'SQLQuery': "SELECT * FROM mobiles",
        'SQLResult': "Result of the SQL query",
        'Answer': "No"
    },
    {
        'Question': "Can you recommend a phone with a high storage capacity for gaming?",
        'SQLQuery': "SELECT model FROM mobiles WHERE storage_capacity > 128 ORDER BY storage_capacity DESC;",
        'SQLResult': "Result of the SQL query",
        'Answer': "Model 10"
    },
    {
        'Question': "How many white color model 1 mobiles we have available?",
        'SQLQuery': "SELECT count(*) FROM mobiles WHERE color = 'White' AND model = 'Model 1';",
        'SQLResult': "Result of the SQL query",
        'Answer': "50"
    }
 ]
 # Path to the directory containing the downloaded al-minim model
 model_path = r"C:\Users\hp\Downloads\all-MiniLM-L6-v2"

 # Create HuggingFaceEmbeddings instance with the local model path
 embeddings = HuggingFaceEmbeddings(model_name=model_path)

 to_vectorize = [" ".join(str(value) for value in example.values()) for example in few_shots]
 vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)

 example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,  # Number of examples to retrieve
 )

 mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
 Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
 Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
 Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
 Pay attention to use CURDATE() function to get the current date, if the question involves "today".

 Use the following format:

 Question: Question here
 SQLQuery: Query to run with no pre-amble
 SQLResult: Result of the SQLQuery
 Answer: Final answer here

 No pre-amble.
 """
 example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
 )
 few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
 )
 chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
 return chain
 


 

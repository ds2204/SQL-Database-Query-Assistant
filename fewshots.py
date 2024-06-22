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

import ollama

def process_npl(prompt):
    system_prompt = ("""
        You are an expert in converting English prompts into and SQL queries!

        Table schema:             
        CREATE TABLE IF NOT EXISTS phonebook (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
        )
        
        Ensure the SQL query is syntactically correct and uses standard SQL syntax.
        Your answer should not have '```' in the beginning or at the end.
        Output only SQL query.
        If prompt can not be converted to SQL return 'COULDNT CONVERT TO SQL'
    """)
    
    response = ollama.generate(model="llama3.2", system=system_prompt, prompt=prompt, options={'temperature': 0})
    sql_response = response['response'].strip()
    sql_lines = [line for line in sql_response.split("\n") if line.strip().startswith(("SELECT", "INSERT", "UPDATE", "DELETE"))]
    return sql_lines[-1] if sql_lines else "COULDNT CONVERT TO SQL"
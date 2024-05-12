import models, sql

class Chat:
    def __init__(self, sql_data_path, sql_coder_dir, llm_path, sql_prompt_structure_path, llm_prompt_structure_path):
        self.data_path = sql_data_path
        self.db_structure = sql.print_db_structure(sql_data_path, 2)
        
        self.sql_model, self.sql_token  = models.get_coder(sql_coder_dir)

        self.llm = models.get_llm(llm_path)

        with open(sql_prompt_structure_path, "r") as prompt_structure:
           self.sql_prompt = prompt_structure.read()

        with open(llm_prompt_structure_path, "r") as prompt_structure:
           self.llm_prompt = prompt_structure.read()

    
    def answer(self, question, print_prompts=False):
        prompt_1 = models.format_sql_prompt(self.sql_prompt, self.db_structure, question)
        sql_query = models.get_sql_query(self.sql_model, self.sql_token, prompt_1)

        if print_prompts:
          print(f"SQL Query:\n{prompt_1}")

        retreived_context = sql.get_query_output(self.data_path, sql_query)
        if retreived_context is False or len(retreived_context) == 0:
            return "Unable to generate SQL query"

        prompt_2 = models.format_llm_prompt(self.llm_prompt, retreived_context.to_string(), question)

        if print_prompts:
          print(f"Output:\n{retreived_context}", end="\n\n")
          print(f"LLM Prompt:\n{prompt_2}")

        llm_response = models.get_llm_response(self.llm, prompt_2)

        if print_prompts:
          print(f"Output:\n{llm_response}")

        return llm_response

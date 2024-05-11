import os
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
import sqlparse
from llama_cpp import Llama


def set_up_coder(save_dir: str):
    available_memory = torch.cuda.get_device_properties(0).total_memory
    model_name = "defog/sqlcoder-7b-2"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if available_memory > 17e9:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=True,
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            # torch_dtype=torch.float16,
            load_in_4bit=True,
            device_map="auto",
            use_cache=True,
        )
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)

    return model, tokenizer


def get_coder(save_dir: str):
    model = AutoModelForCausalLM.from_pretrained(save_dir)
    tokenizer = AutoTokenizer.from_pretrained(save_dir)
    
    return model, tokenizer


def get_sql_query(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    generated_ids = model.generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=1,
    )
    outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    return sqlparse.format(outputs[0].split("[SQL]")[-1], reindent=True)


def get_llm(model_path: str):
    return Llama(
      model_path=model_path,
      n_gpu_layers=-1,
      n_batch=512,
      n_threads=2,
      verbose=True
)


def get_llm_response(llm, prompt):
    return llm(
        prompt,
        max_tokens=256,
        temperature=0.2,
        echo=True
    )["choices"][0]['text'][len(prompt):]

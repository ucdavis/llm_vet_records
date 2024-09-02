import re
import json
import tiktoken
import time

from openai import AzureOpenAI
import openai

with open("openai_key.txt", "r") as f:
	api_key = f.read().strip()
    
client = AzureOpenAI(
    api_key=api_key,  
    api_version="2024-02-01",
    azure_endpoint = "https://gpt-4-turbo-fce.openai.azure.com/"
    )
    
deployment_name='gpt-4o' 

expected_keys = {
    "case_number",
    "appetite_reference",
    "decreased_appetite",
    "polyphagia",
    "vomiting_reference",
    "vomiting",
    "defecation_reference",
    "diarrhea",
    "constipation",
    "weight_reference",
    "weight_loss"
  }

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def execute_prompt(phrase, temperature):
	response = client.chat.completions.create(
		model=deployment_name, 
		messages = [{"role":"system", "content": phrase}],
		temperature=temperature
		)
	return response.choices[0].message.content

def process_response(response, case_number, num_input_tokens, elapsed_time, 
prompt, record_text, temperature, iteration):
	json_blocks = re.findall(r"(?:```json)(.*?)(?:```)", response, re.DOTALL)
	if len(json_blocks) == 0:
		json_blocks = [response]
	if len(json_blocks) != 1: 
		return {
		"case_number": case_number, 
		"status": "wrong number of json blocks", 
		"response": response,
		"temperature": temperature,
		"iteration": iteration
		}
	try: 
		data = json.loads(json_blocks[0])
	except:
		return {
		"case_number": case_number, 
		"status": "couldn't parse json", 
		"response": response,
		"temperature": temperature,
		"iteration": iteration
		}
	if set(data.keys()) != expected_keys:
		return {
		"case_number": case_number, 
		"status": "wrong keys", 
		"response": response,
		"temperature": temperature,
		"iteration": iteration
		}
	if data["case_number"] != case_number:
		return {
		"case_number": case_number, 
		"status": "wrong case number", 
		"response": response,
		"temperature": temperature,
		"iteration": iteration
		}
	data["status"] = "ok"
	data["num_output_tokens"] = num_tokens_from_string(response)
	data["num_input_tokens"] = num_input_tokens
	data["elapsed_time"] = elapsed_time
	data["prompt"] = prompt
	data["record"] = record_text
	data["temperature"] = temperature
	data["iteration"] = iteration
	return data
		
with open("prompt.txt", "r") as f:
	prompt_template=f.read()


with open("test.json", "r") as f:
	records=json.loads(f.read())

temperatures = [0, 0.5, 1]
iterations = 5
output = []

for temp in temperatures: 
	for iteration in range(1, iterations + 1):
		for record in records:
			print(f"Processing case {record['case']} with temperature {temp} and iteration {iteration}")
			prompt = prompt_template.replace("<MEDICAL_RECORD>", json.dumps(record))
			record_text = json.dumps(record)
			temperature = temp
			start_time = time.time()
			try: 
				response = execute_prompt(prompt, temperature = temp)
				stop_time = time.time()
				output.append(process_response(response, record["case"], 
				num_tokens_from_string(prompt), stop_time-start_time, prompt, 
				record_text, temperature, iteration))
			except json.JSONDecodeError:
				output.append({
					"case_number": record["case"],
					"status": "couldn't parse json",
					"response": "",
					"temperature": temp,
					"iteration": iteration
				})
			except UnicodeEncodeError:
				output.append({
					"case_number":record["case"],
					"status": "output not in unicode",
					"response":"",
					"temperature": temp,
					"iteration": iteration
				})
			except Exception as e:
				output.append({
				"case_number": record["case"],
				"status": "invalid unicode output",
				"response":str(e),
				"temperature": temp,
				"iteration": iteration
				})
	
with open("output.json", "w") as f:
	f.write(json.dumps(output, indent=4))

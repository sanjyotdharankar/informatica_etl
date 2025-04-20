from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Step 1: Load fine-tuned model and tokenizer
model_path = "../etl_llama_model/final"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Step 2: Define a function to generate PySpark code from a prompt
def generate_code(prompt, max_new_tokens=300):
    input_text = f"### Prompt:\n{prompt}\n\n### Completion:\n"
    inputs = tokenizer(input_text, return_tensors="pt").to("cuda")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.2,
            top_p=0.95,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Only return the generated code after '### Completion:'
    if "### Completion:" in generated_text:
        return generated_text.split("### Completion:")[1].strip()
    else:
        return generated_text.strip()

# Step 3: Provide a new prompt for testing
new_prompt = """Source: employee.csv, Target: employee_clean.parquet, Mappings: emp_id->employee_id, emp_name->name, emp_dept->department, Filter: emp_status='Active', Transform: upper(emp_name)"""

# Step 4: Generate PySpark code
generated_code = generate_code(new_prompt)

# Step 5: Display the result
print("\n🔹 Generated PySpark Code:\n")
print(generated_code)

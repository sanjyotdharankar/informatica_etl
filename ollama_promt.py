import os
import subprocess

def convert_mappings_to_pyspark(input_dir, output_dir, model="mistral"):
    os.makedirs(output_dir, exist_ok=True)

    def create_prompt(md_content):
        return f"""
You are a data engineer. Convert the following Informatica mapping (written in Markdown) into equivalent PySpark code that reads from a SQL Server table, performs transformation logic like lookups, expressions, and routing, and writes the final data to a Parquet file or SQL target.

Only return PySpark code in your output, no explanations.

{md_content}
"""

    def generate_code_with_ollama(prompt):
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=prompt.encode())
        if stderr:
            print("⚠️ Error:", stderr.decode())
        return stdout.decode()

    for filename in os.listdir(input_dir):
        if filename.endswith(".md"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".md", ".py"))

            print(f"🛠️ Processing: {filename}")
            with open(input_path, 'r',encoding="latin-1") as f:
                md_content = f.read()

            prompt = create_prompt(md_content)
            generated_code = generate_code_with_ollama(prompt)

            with open(output_path, 'w') as f_out:
                f_out.write(generated_code)
            print(f"✅ Output saved to: {output_path}\n")



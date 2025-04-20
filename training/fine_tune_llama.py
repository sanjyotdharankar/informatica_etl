# other.py

from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

def fine_tune_model():
    # Step 1: Load Code LLaMA base model (7B Python model for example)
    model_name = "codellama/CodeLlama-7b-Python-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Optional: Set padding side and EOS token
    tokenizer.pad_token = tokenizer.eos_token

    # 4-bit quantization for efficiency
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_4bit=True,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Step 2: Apply PEFT with LoRA
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_config)

    # Step 3: Load your JSONL training dataset
    dataset = load_dataset("json", data_files="../train_advanced.jsonl", split="train")

    # Step 4: Tokenization function
    def tokenize(example):
        full_prompt = f"### Prompt:\n{example['prompt']}\n\n### Completion:\n{example['completion']}"
        tokens = tokenizer(full_prompt, truncation=True, padding="max_length", max_length=2048)
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    # Apply tokenization
    tokenized_dataset = dataset.map(tokenize, batched=False)

    # Step 5: Define training parameters
    training_args = TrainingArguments(
        output_dir="../etl_llama_model",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        fp16=True,
        logging_steps=5,
        save_steps=50,
        evaluation_strategy="no",
        save_total_limit=1,
        learning_rate=2e-4,
        report_to="none"
    )

    # Step 6: Data collator for causal language modeling
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    # Step 7: Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator
    )

    # Step 8: Start fine-tuning
    trainer.train()

    # Step 9: Save final fine-tuned model and tokenizer
    # C:\Users\sanjy\Downloads\informaticail\etl_llama_model\final
    model.save_pretrained("../../etl_llama_mode/final")
    tokenizer.save_pretrained("../../etl_llama_mode/final")

    print("✅ Fine-tuning complete! Model saved in informaticail/final")

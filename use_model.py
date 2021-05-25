from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModelling
from datasets import load_dataset # pip3 install datasets
from transformers import Trainer, TrainingArguments

TRAIN_BASE = False
paths = ["python_code_data.txt"]

if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    # Save files to disk
    tokenizer.save_model("tokenizer")

inp = "print('Hello World')"
tokenizer = GPT2Tokenizer.from_pretrained("tokenizer")

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

t = tokenizer.encode(inp)
print(t)

print(tokenizer.decode(t))

model = GPT2LMHeadModel.from_pretrained("GPyT").to("cuda")

while True:
    inp = input(">>> ")
    input_ids = tokenizer.encode(inp, return_tensors="pt").to("cuda")
    beam_output= model.generate(
        input_ids,
        max_length = 512,
        num_beams = 10,
        temperature = 0.7,
        no_repeat_ngram_size = 5,
        num_return_sequences = 1
    )
    for beam in beam_output:
        out = tokenizer.decode(beam)
        fout = out.replace("<N>", "\n")

        print(green(str(fout)))
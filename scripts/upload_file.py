import openai, sys

openai.api_key, file_path = sys.argv[1], sys.argv[2]

with open(file_path, "rb") as f:
    file_obj = openai.files.create(file=f, purpose='fine-tune')

print(file_obj.id)


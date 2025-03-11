import openai, sys

openai.api_key, file_id = sys.argv[1], sys.argv[2]

fine_tune_response = openai.fine_tuning.jobs.create(
    training_file=file_id, 
    model="gpt-3.5-turbo"
)
print(fine_tune_response.id)


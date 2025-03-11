import openai, sys, time

openai.api_key, job_id = sys.argv[1], sys.argv[2]

while True:
    status = openai.fine_tuning.jobs.retrieve(job_id)
    current_status = status.status
    print(current_status)

    if current_status in ['succeeded', 'failed', 'cancelled']:
        if current_status == 'succeeded':
            print(f"{current_status},{status.fine_tuned_model}")
        else:
            print(f"{current_status},")
        break
    time.sleep(30)  # 增加等待间隔，避免API调用过于频繁

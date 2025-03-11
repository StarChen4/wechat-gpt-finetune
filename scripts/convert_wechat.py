import re, json, sys, os

filename, target_name = sys.argv[1], sys.argv[2]

with open(filename, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

dialogs, i = [], 0
while i < len(lines)-1:
    match = re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (.+)', lines[i])
    if match:
        dialogs.append({'speaker': match.group(1), 'content': lines[i+1]})
        i += 2
    else:
        i += 1

training_data, i = [], 0
while i < len(dialogs)-1:
    if dialogs[i]['speaker'] != target_name and dialogs[i+1]['speaker'] == target_name:
        training_data.append({
            "messages":[
                {"role":"system","content":f"你是模仿{target_name}风格的AI助手。"},
                {"role":"user","content":dialogs[i]['content']},
                {"role":"assistant","content":dialogs[i+1]['content']}
            ]
        })
        i += 2
    else:
        i += 1

output_path = filename.replace('.txt', '_train.jsonl')
with open(output_path:=output_path, 'w', encoding='utf-8') as f:
    for item in training_data:
        f.write(json.dumps(item, ensure_ascii=False)+'\n')

print(output_path)

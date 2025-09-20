import json

with open("tempdataset.jsonl") as f:
    datas = []
    filtered = open("newdata.json", "a")
    for line in f.readlines():
        data = json.loads(line)
        if "furina" not in data.get("input").lower():
            datas.append(data)
            
    filtered.write(json.dumps(datas))
    filtered.close()
import re

def insert_before_num(input_str,ins_str):
    return re.sub(r'\d',ins_str+re.search( r'\d', input_str, re.M|re.I).group(0),input_str,count=1)

def insert_before_num2(input_str,ins_str):
    index=re.search(r'\d',input_str).start()
    return input_str[:index]+ins_str+input_str[index:]
print(insert_before_num2('./json/air-hole2-13.json','(crack)'))

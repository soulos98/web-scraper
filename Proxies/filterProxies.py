import pandas as pd
import requests
import queue
import threading
# http://ipinfo.io/json


q = queue.Queue()
workingProxies = []


def checkProxies(proxy: str):

    statusCode = 0
    http_proxy = "http://" + proxy
    https_proxy = "https://" + proxy
    try:
        res = requests.get("http://ipinfo.io/json",
                           proxies={"http": http_proxy, "https": https_proxy})
        print(proxy)
        statusCode = res.status_code

    except:
        return ""

    # print(proxy if statusCode == 0 else "")

    return proxy if statusCode == 200 else ""


def filterProxies() -> list[str]:
    global q
    global workingProxies

    while q.qsize() > 0:
        proxy = q.get()
        res = checkProxies(proxy)
        if res:
            print(res)
            workingProxies.append(res)


proxiesData = pd.read_csv("proxies.csv")
df = pd.DataFrame(proxiesData, columns=['ip', 'port'])

df_List = df.values.tolist()

for row in range(len(df_List)):
    proxy = ':'.join(str(proxy_part) for proxy_part in df_List[row])
    q.put(proxy)
# df_List = str"ip:port"

threads = []
for _ in range(10):
    thread = threading.Thread(target=filterProxies)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(
    f"Original List length {len(df_List)} \nNew List length {len(workingProxies)}")

filtered = open('filteredProxies.txt', 'w')

filtered.write(workingProxies)

filtered.close()

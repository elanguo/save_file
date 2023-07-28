#这是0713-2.1，目的是自动从文件"pantherGeneList.txt"中，拿到每一个蛋白的的uniprot id，然后去Uniprot里找到其蛋白序列，并生成一个fasta
import requests  #导入requests模块
from requests.exceptions import Timeout  #从 requests模块的exceptions子模块中导入Timeout异常。Timeout异常在请求超时会允许处理。

#定义通过uniprot id自动抓取蛋白序列的方程
def fetch_protein_sequence(uniprot_id):  #定义抓取对应蛋白序列的函数
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    #f-string格式，用于访问网站并查找某Uniprot ID
    print(uniprot_id)  #显示Uniprot ID
    try:  #处理异常代码
        response = requests.get(url, timeout=10)  #向构建好的URL发送HTTP GET请求，同时设置了请求超时时间为10秒
        if response.ok:
            #解析fasta格式的响应内容，提取蛋白质序列
            lines = response.text.strip().split("\n")  #响应内容以字符串形式获取，用strip()去除空白，然后用将内容按行切割成列表
            sequence = "".join(lines[1:])  #忽略第一行以>开头的蛋白质标识信息，从第二行开始连成字符串，得到完整蛋白序列，存入sequence中
            return sequence  #如果抓取成功，函数返回从Uniprot获取的蛋白质序列数据
        else:
            return None  #如果响应失败，则返回None
    except Timeout:
        return None  #如果请求超时，函数返回None表示抓取失败

with open("pantherGeneList.txt", "r") as input_file, open("output_new.fasta", "w") as output_file:  #打开两个文件并重命名
    list_id = []
    count = 0
    for line in input_file:
        if not line.strip():  #判断行是否为空或者只包含换行符
            continue
        count += 1  #如果不是空白行，则+1
        columns = line.strip().split("\t")   #把input不为空白行的数据，去掉首尾空白并以tab分隔，储存在列表columns里
        if len(columns) > 0:
            #解析UniProt ID和连接的最后一列
            uniprot_id = columns[0].split("UniProtKB=")[-1]   #column第一列的数据，根据UniProtKB=分成两部分，取第二部分，得到uniport id
            last_column = columns[-1]   #得到物种名称
            full_id = f"{uniprot_id}_{last_column}"   #合成完整的id
            list_id.append(uniprot_id) #将uniprot id数据填入list_id中
            retries = 5
            while retries > 0:
                sequence = fetch_protein_sequence(uniprot_id)
                if sequence:
                    print(f"Processing protein {count}")
                    output_file.write(f">{full_id}\n")
                    output_file.write(f"{sequence}\n")
                    break
                    #如果抓取成功，则在output里打出full_id且换行，在打出sequence结果即蛋白序列，然后空行，跳出此while循环
                else:
                    retries -= 1
                    print(f"Retrying protein {count}, remaining retries: {retries}")
            if retries == 0:
                print(f"Failed to fetch protein {uniprot_id}")
            #如果没抓取到则重试，到第五次如果还没抓取到则显示失败，并开始抓取下一个

#0713-2.2，检查重要蛋白
with open("output_new.fasta", "a") as output_file:   #以追加写入模式打开文件并重命名
    #上网收集重要蛋白质的uniprot id和名称
    list_cruical = ['C0SVZ6', 'C6L7V8', 'C6L7V9']
    list_name = ['Curcumin synthase 1', 'Curcumin synthase 2', 'Curcumin synthase 3']
    if not set(list_cruical).intersection(set(list_id)):   #检查两个列表交集是否为空
        for i in range(3):  #循环3次，分别对应三组数据
            uniprot_id = list_cruical[i]
            last_column = list_name[i]
            full_id = f"{uniprot_id}_{last_column}"
            retries = 5
            while retries > 0:
                sequence = fetch_protein_sequence(uniprot_id)   #进入循环，尝试抓取蛋白序列5次
                if sequence:
                    print(f"Processing protein {count}")
                    output_file.write(f">{full_id}\n")
                    output_file.write(f"{sequence}\n")
                    break
                else:
                    retries -= 1
                    print(f"Retrying protein {count}, remaining retries: {retries}")
            if retries == 0:
                print(f"Failed to fetch protein {uniprot_id}")
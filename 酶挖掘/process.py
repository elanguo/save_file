#在output基础上，给每个蛋白添加protein id，形成output processed
with open('output_new.fasta', 'r') as file:
    ID = []
    for line in file:
        if line.startswith('>'):
        #是否以“>”符号开头是FASTA文件中蛋白质标识的特点，用于判断是否为蛋白质标识行
            line = line.strip('\n').split('_')   #将每行line数据去掉首尾换行符，根据“_”分割开
            line = line[0].strip('>')   #将每行line数据第一项去除首尾“>”，存回line
            ID.append(line)   #将line数据存入ID
#标识的格式类似于>uniprotid_proteinname，使用下划线分割后得到一个包含两个元素的列表，第一个元素是 UniProt ID，第二个元素是蛋白质名称
#取列表的第一个元素，即uniprot id，然后去除字符串开头“>”，得到干净的uniprot id


with open('output_1.tsv', 'r') as input_1:
    x = input_1.readlines()  #将文件每一行数据存入x
    list1 = []
    for i in x:  #对于x中的每一行
        line = i.strip('\n').split()   #每行数据去掉换行符，根据空格分开，存回
        list1.append(line)   #line数据存入列表list 1
    list1[0].append('Protein ID')  #在list 1第一行末尾前加入空白表头Protein ID
    for i in range(len(list1)):
        if i == 0:
            continue   #如果到达表头行，则跳过
        else:
            list1[i].append(ID[i-1])  #如果是数据行，在末尾加入对应的干净的uniprot id
                                      #因为列表ID没有表头，所以要错开对齐

with open('output_1_processed.tsv','w') as output:
    for i in list1:
        line = '\t'.join(i)   #对于list1的一行数据，用空格将每一个数据隔开，变成字符串，赋值给line
        output.write(line + '\n')   #将一行字符串line写入文件，并换行
#如此一行一行处理，构建出文件output_1_processed.tsv

with open('output_2.tsv', 'r') as input_2:
    x = input_2.readlines()
    list1 = []
    for i in x:
        line = i.strip('\n').split()
        list1.append(line)
    list1[0].append('Protein ID')
    for i in range(len(list1)):
        if i == 0:
            continue
        else:
            list1[i].append(ID[i-1])

with open('output_2_processed.tsv','w') as output:
    for i in list1:
        line = '\t'.join(i)
        output.write(line + '\n')
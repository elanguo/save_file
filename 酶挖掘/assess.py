#tidy两个文件
Substrate_Name = ['Feruloyl-CoA', 'coumaroyl-CoA']  #定义底物名称
SMILES = ['CC(C)(COP(=O)([O-])OP(=O)([O-])OC[C@@H]1[C@H]([C@H]([C@@H](O1)N2C=NC3=C(N=CN=C32)N)O)OP(=O)([O-])[O-])[C@H](C(=O)NCCC(=O)NCCSC(=O)/C=C/C4=CC(=C(C=C4)O)OC)O', 'CC(C)(COP(=O)(O)OP(=O)(O)OC[C@@H]1[C@H]([C@H]([C@@H](O1)N2C=NC3=C(N=CN=C32)N)O)OP(=O)(O)O)[C@H](C(=O)NCCC(=O)NCCSC(=O)/C=C/C4=CC=C(C=C4)O)O']  #定义底物化学式
with open('output_new.fasta', 'r') as file:  #以阅读模式打开名为output_new.fasta的文件，并命名为file
    sequences = []  #建立空列表
    for line in file:
        if line.startswith('>'):
            pass  #如果file中的某一行以>打头，则跳过这一行
        else:
            line = line.strip('\n')  #对不以>打头的行，去掉行尾换行符
            sequences.append(line)  #将处理好的file数据存进列表sequences中
print(sequences)  #显示sequences
data_1 = []
data_2 = []  #建立空列表
data_1.append(['Substrate Name', 'Substrate SMILES', 'Protein Sequence'])
data_2.append(['Substrate Name', 'Substrate SMILES', 'Protein Sequence'])  #建立两个只有表头的空列表
for i in sequences:
    m = []  #建立空列表m
    m.append(Substrate_Name[0])  #将Substrate_Name索引为0的数据存入
    m.append(SMILES[0])  #将SMILES索引为0的数据存入
    m.append(i)  #将i存入m中
    data_1.append(m)  #将m存入data_1中
for i in sequences:
    m = []
    m.append(Substrate_Name[1])
    m.append(SMILES[1])
    m.append(i)
    data_2.append(m)  #用同样方法，将第二组数据存入
with open('input_1.tsv', 'w') as file:  #以写入模式打开文件input_1.tsv，并命名为file
    for row in data_1:  #对于列表data_1中的每一行数据
        line = '\t'.join(str(cell) for cell in row)  #将每一行的三个数据都转换成字符串，并用tab分隔连接，储存到line中
        file.write(line + '\n')  #用分行符将line的每行数据隔开，输入回file中
with open('input_2.tsv', 'w') as file:
    for row in data_2:
        line = '\t'.join(str(cell) for cell in row)
        file.write(line + '\n')  #用相同的方法重新整理input_2.tsv
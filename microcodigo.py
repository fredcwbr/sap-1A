import csv


FMicroCodigo = 'microcodigo.csv'


bitsControle = ['PCLD',
       'PCCNT_e',
       'PCCOUT_e',
       'NXT_I',
       'RInst_E',
       'DIRECTAddr_e',
       'ADDRRAM_e',
       'ACC_E',
       'ALU_RSLT_e',
       'ALU_OUT_e',
       'RAM_e',
       'IO_e',
       'ALU_SUB',
       'ALU_INV',
       'ALU_CYIN',
       'WR/~RD'
       ]


with open(FMicroCodigo, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file,  delimiter='\t')
    line_count = 0
    for row in csv_reader:
        if row['Id'] not in ['x','I','X']:
            # despreza comentarios
            continue
        # cria o micro codigo
        I = row['Instrucao']
        T = row['Tempo']
        # combina os 16 bits do barramento de controle
        #
        print( '{:04b}'.format(int(I)) , '{:03b}'.format(int(T)) , ''.join([ row[B] for B in bitsControle   ] ) )
        
        
        
        
    

import csv
from intelhex import IntelHex
import sys


arquivoMicrocodigo = "microcodigo.hex"
ih = IntelHex()
ih.padding = 0x00 

FMicroCodigo = 'microcodigo.csv'


bitsControle = {
       0: 'PCLD',
       1: 'PCCNT_e',
       2: 'PCCOUT_e',
       3: 'NXT_I',
       4: 'RInst_E',
       5: 'DIRECTAddr_e',
       6: 'ADDRRAM_e',
       7: 'ACC_E',
       8: 'ALU_RSLT_e',
       9: 'ALU_OUT_e',
      10: 'RAM_e',
      11: 'IO_e',
      12: 'ALU_SUB',
      13: 'ALU_INV',
      14: 'ALU_CYIN',
      15: 'WR/~RD'
       }

nBitsInstrucao = 4
# Indice o uCodigo = Codigo da instrucao
# Total de instrucoes possiveis >> 2^nBitsInstrucao -1 .
# o RANGE no python é de dominio aberto , ... até (n-1) comecando em 0 ... 


F = open('microcodigo.hex','w')
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
        uCodigo = [0,0]
        addruInstr = '0b{:04b}{:03b}'.format(int(I),int(T))
        for BT in range(0,2):
            bControle = '0b'+''.join([ row[bitsControle[(BT*8)+ndx]] for ndx in range(0,8) ])
            uCodigo[BT] = int(bControle, 2)
        print(  int(addruInstr,2) , addruInstr ,'{:04b}'.format(int(I)) ,bControle, '{:03b}'.format(int(T)) , uCodigo  )

        for I in range(len(uCodigo)):
            ih[int(addruInstr,2)+int(T)*len(uCodigo)+I] = uCodigo[I]

ih.write_hex_file(sys.stdout)
ih.write_hex_file(arquivoMicrocodigo)
        
        
    

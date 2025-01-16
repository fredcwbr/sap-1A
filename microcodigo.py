import csv
import sys


arquivoMicrocodigo = "microcodigo.hex"
#ih = IntelHex()
#ih.padding = 0x00 

"""
Formato do arquivo hex do Digital HNeeman
v2.0 raw
>> uma linha por endereco

"""
class hneemanHex:
    def __init__(self, fname):
        self.conteudo = {}
        self.fname = fname

    def addValue(self, addr, value):
        self.conteudo[addr] = value

    def geraHex(self):
        with open(self.fname,'w') as F:
           print( 'v2.0 raw', file=F )
           Add = 0
           print( dict(sorted(self.conteudo.items())) )
           for A, V in dict(sorted(self.conteudo.items())).items():
               if A != Add:
                    print( '{}*0'.format( A - Add ) , file=F)
                    Add = A
               print( '{:4X}'.format( V ) , file=F)
               Add = Add + 1
                
            
     


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

F = hneemanHex(arquivoMicrocodigo)

instrPopulados = []
with open(FMicroCodigo, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file,  delimiter='\t')
    line_count = 0
    for row in csv_reader:
        if row['Id'] not in ['x','I','X']:
            # despreza comentarios
            continue
        # cria o micro codigo
        I = row['Instrucao']
        instrPopulados.append(int(I))
        T = row['Tempo']
        # combina os 16 bits do barramento de controle
        #                
        addruInstr = int( '0b{:04b}{:03b}'.format(int(I),int(T)) , 2)

        for BT in [1,0]:
                print( [ row[bitsControle[(BT*8)+ndx-1]] for ndx in range(8,0,-1) ] )
                
                # bControle = '0b'+''.join([ row[bitsControle[(BT*8)+ndx]] ])
        bControle = '0b'+''.join([ row[bitsControle[(BT*8)+ndx-1]] for BT in [1,0] for ndx in range(8,0,-1) ])                
        # bControle = '0b'+''.join([ row[bitsControle[(BT*8)+ndx]] for BT in [1,0] for ndx in range(0,8) ])
        
        print(  '{:04b}'.format(int(I)), addruInstr , addruInstr ,'{:04b}'.format(int(I)) ,bControle, '{:03b}'.format(int(T)) ,bControle  )
        F.addValue( addruInstr,  int(bControle, 2) )

S = [ X for X in range(16) if X not in instrPopulados ]
for I in S:
    addruInstr = int( '0b{:04b}{:03b}'.format(int(I),0) , 2)
    F.addValue( addruInstr,  0b10100 )
    
        
F.geraHex()

    

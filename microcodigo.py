#!/usr/bin/env python3

import csv
import sys
import yaml



"""
Versao usando o uCodigo em yaml .,

"""
arquivoMicrocodigo = "microcodigo.hex"


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

def uInstrucao( codigo, passos ):
    # Tempos dessa instrucao
    uC = {}
    print( codigo, passos )
    for P in range(len(passos) ):
        addruInstr = int( '0b{:04b}{:03b}'.format(codigo,P), 2)
        bC = 0
        for x in [ 1<<b for b in passos[P] ]:
            bC |= x
        uC[addruInstr] =  bC
        print(  codigo, P, '@{:04b}{:03b}'.format(codigo, P) , '{:016b}'.format(bC), '{:04X}'.format(bC) )
    return uC
     
# Fonte do microcodigo
uCodigoFonte = 'microcodigo.yaml'
with open(uCodigoFonte,'rt', encoding='utf-8') as uC:
    uCodigo = yaml.safe_load(uC)

# 
# controlBusBits
#
# Esta no yaml e agora tem o controle do barramento
# os Bits estao codificados com as instrucoes e as
# micro instrucoes de HW.,
# Ajudara na sintaxe para o assembler,.


# LUT  do microcodigo para o DIGITAL
FMicroCodigo = 'microcodigo.hex'
F = hneemanHex(arquivoMicrocodigo)
#

nBitsInstrucao = 4
# Indice o uCodigo = Codigo da instrucao
# Total de instrucoes possiveis >> 2^nBitsInstrucao -1 .
# o RANGE no python é de dominio aberto , ... até (n-1) comecando em 0 ... 

instrPopulados = []
for opCd, Det in uCodigo['opCodes'].items():
    if Det['cdInstrucao'] is None:
        continue
    instrPopulados.append(Det['cdInstrucao'])
    for K,V in uInstrucao( Det['cdInstrucao'], Det['uCodigo'] ).items():
        F.addValue( K,V )

S = [ X for X in range(16) if X not in instrPopulados ]
for I in S:
    for K,V in uInstrucao( I, uCodigo['opCodes']['NOP']['uCodigo'] ).items():
        F.addValue( K,  V  )
    
        
F.geraHex()

    

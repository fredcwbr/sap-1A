#!/usr/bin/env python3

import os
import sys
import yaml
import re


brancos = {"\t":' ', "\v": ' ' }



# Fonte do Programa
if len(sys.argv) > 1:
    cdFonte = sys.argv[1]
else:
    cdFonte = 'Sap1A_Ex02.asm'
    
# Fonte do microcodigo
uCodigoFonte = 'microcodigo.yaml'


fResult =  [ 'lst', 'hex' ]

rWords = [ 'DB' ]
eWords = [ 'EQU', 'ORG' ]

with open(uCodigoFonte,'rt', encoding='utf-8') as uC:
    uCodigo = yaml.safe_load(uC)

"""
lbl:  opCode  Vl
;
;
;
opCodes

NOP None
HLT 15
LDMA 1
LDIRAM 2
LDIACC 3
LDRAM2ACC 4
ADD 5
SUB 6
ST 7
JMP 8
JZ 9
JNEG 10
IOR 12
IOW 13

KY = opCode,
cdInstrucao ;
; 
;             
;
"""
passos = []



def monta( seq, instr, operando ):
    # trata operando com possibilidade de informacao 
    # em hex , octal ou decimal
    #
    if not isinstance(operando,int):
        operando = operando.upper()
        if 'X' in operando:
            # converte de hexa.,
            OPx= int(operando.split('X')[1],16)
        elif 'O' in operando.upper():
            # converte de octal.,
            OPx= int(operando.split('O')[1],8)
        elif 'B' in operando.upper():
            # converte de binario.,
            OPx= int(operando.split('B')[1],2)
        else:
            OPx= int(operando)  # Decimal
    else:
        OPx = int(operando)
    codObj = '{OP:04X}{INSTR:01X}'.format(
                OP = OPx,
                INSTR=int(uCodigo['opCodes'][instr]['cdInstrucao'])
                )
    return codObj, seq, instr, operando ,uCodigo['opCodes'][instr]['cdInstrucao']

def lSplit( strx ):
    x = [None, None, None]
    if strx.strip() == '' or str is None:
        return x
    if ':' in strx:
        lbl, lin = re.split( r':', strx )
    else:
        lbl = None
        lin = strx
    X = re.split( '\s' , lin.strip() )
    for I in range(len(X)):
        x[I] = X[I].strip().upper()
    return lbl, x[0], x[1]

# Le arquivo fonte,
# split do arquivo
#   label  : operando   vl/@end
#
with open(cdFonte,'rt') as F:
    # instrucoes :::
    # Le tudo .,
    cd = F.readlines()

lblS = {}
# Pass1  --> Enderecos de variaveis
cntRAM = 0
for L in cd:
    lbl, opCode, valor = lSplit( L.replace('\t', ' ') )
    if opCode in rWords:
        lblS[lbl.upper()] = cntRAM
        cntRAM = cntRAM + 1
    elif opCode in eWords:
        # EQU ou ORG ,
        lblS[lbl.upper()] = valor
    elif lbl is not None:
        lblS[lbl.upper()] = None  # No codigo, ainda nao sabemos o endereco ., 

# Pass 2 -->
# Enderecos das instrucoes
cntPgm = 0
passos = {}
for L in cd:
    lbl, opCode, valor = lSplit( L.replace('\t', ' ')  )
    if opCode in rWords or opCode in eWords or opCode is None:
        # Alocacao de memoria RAM é so designativa
        continue  
    else:
        passos[cntPgm] = [ opCode, lbl , valor ]
        if lbl is not None:
            lblS[lbl.upper()] = cntPgm  # Agora sabemos o endereco .. .
        cntPgm = cntPgm + 1

# Pass 3
# dump known labels and values
print( '\n'.join( '{} {}'.format( L, addr ) for L,addr in lblS.items() ) )

FNhex = cdFonte.split('.')[0] + '.hex'
FNlst = cdFonte.split('.')[0] + '.lst'
fhex = open( FNhex, 'w' )
print( 'v2.0 raw', file=fhex )
flst = open( FNlst, 'w' )

for L, (opCode, lbl , valor) in passos.items():
    if valor in lblS:
        operando = lblS[valor]
    else:
        operando = valor
    codObj, sq, inst, op ,ciop = monta( L, opCode, operando )
    print(codObj, file=fhex)
    print( '{:02x}'.format(sq), codObj, sq, inst, op ,ciop, file=flst )

fhex.close()
flst.close()






import os
import sys
import yaml
import re

cdFonte = 'Sap1A_Ex01.asm'
fResult =  [ 'lst', 'hex' ]

rWords = [ 'DB' ]
eWords = [ 'EQU', 'ORG' ]


# Fonte do microcodigo
uCodigoFonte = 'microcodigo.yaml'
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
    codObj = '{OP:04X}{INSTR:01X}'.format(
                OP=int(operando),
                INSTR=int(uCodigo['opCodes'][instr]['cdInstrucao'])
                )
    return codObj, seq, instr, operando ,uCodigo['opCodes'][instr]['cdInstrucao']

def lSplit( strx ):
    x = [None, None, None]
    # print(strx)
    if strx.strip() == '' or str is None:
        return x
    if ':' in strx:
        lbl, lin = re.split( r':', strx )
    else:
        lbl = None
        lin = strx
    X = re.split( r'\s' , lin.strip() )
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
    lbl, opCode, valor = lSplit( L )
    if opCode in rWords:
        lblS[lbl] = cntRAM
        cntRAM = cntRAM + 1
    elif opCode in eWords:
        # EQU ou ORG ,
        lblS[lbl] = valor
    elif lbl is not None:
        lblS[lbl] = None  # No codigo, ainda nao sabemos o endereco ., 

# Pass 2 -->
# Enderecos das instrucoes
cntPgm = 0
passos = {}
for L in cd:
    lbl, opCode, valor = lSplit( L )
    if opCode in rWords or opCode in eWords or opCode is None:
        # Alocacao de memoria RAM é so designativa
        continue  
    else:
        passos[cntPgm] = [ opCode, lbl , valor ]
        if lbl is not None:
            lblS[lbl] = cntPgm  # Agora sabemos o endereco .. .
        cntPgm = cntPgm + 1

# Pass 3

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
    print( codObj, sq, inst, op ,ciop, file=flst )

fhex.close()
flst.close()






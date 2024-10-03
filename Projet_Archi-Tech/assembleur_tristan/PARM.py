from PARM_utils import parm, clean
from time import time

file = "instructions.s"
parm = parm(bavard = False)

def b(n:int, l:int = 3)->str:
    b = bin(int(n) & 2**l-1)[2:]
    return str(int(int(n)<0))*(l-len(b)) + b

def d(n:str, m:int = 16) -> int:
    if len(n) > m:
        return -1
    return int(n, 2)

def val(cmd:str, prm:list)->hex:
    bit = 16
    if cmd in ["str","ldr"] and len(prm)==2: prm.insert(1,"#0")
    if cmd in ["muls","rsbs"]: prm = prm[:-1]
    parm.log(f"log fonction val : {cmd} {prm}")
    
    total = parm.commandes[len(prm)][cmd]
    bit -= len(total)
    if cmd in ["adds","subs"] and prm[-1][0] == "#":
        if len(prm) == 2:
            prm = prm[::-1]
        else:
            total = total[:5]+"1"+total[6:]
    if not cmd in ["str","ldr","movs"] : prm = prm[::-1] #retourne l'ordre des arguments pour les traiter correctement

    taille, div, prs = 0, 1, []
    for i in range(len(prm)):
        if prm[i][0] == "r":
            prs.append((prm[i][-1],3))
            taille += 3
        elif prm[i][0] == "#":
            prs.append((prm[i][1:],-1))
        elif prm[i][0] == "s":
            div = 4

    parm.log("log arguments fonction val : {prs}")
    for e in prs:
        if e[1] == -1:
            total += b(int(e[0])/div,bit-taille)
        else:
            total += b(e[0],e[1])
            taille -= e[1]
            bit -= e[1]
    parm.log(f"log fin de fonction val : {hex(d(total))}")
    return hex(d(total))[2:].zfill(4)


def compile_file(file, compare = None)->[(int, int), None]:
    with open(file,"r") as file: instructions = [i for i in file.read().split('\n') if len(i) > 1 and i[0] != "@"]

    n, hexa, branchs = 0, [], {}
    for i in instructions:
        if len(i) > 1 and i[0] == ".":
            branchs[i.split(".")[1].split(':')[0]] = n
        else:
            n += 1

    instructions = [i for i in instructions if len(i)>0 and i[0] != "."]
    for i in range(len(instructions)):
        instruction = instructions[i]
        try:
            if instruction[0] != ".":
                if '\t' in instruction:
                    cmd, prm = instruction.split('\t')
                else:
                    cmd = instruction.split(' ')[0]
                    prm = ' '.join(instruction.split(' ')[1:])
                prm = [clean(e) for e in prm.split(',')]
                if cmd[0] == "b" and cmd[:4] != "bics":
                    prm = ["#" + str(branchs[instruction.split('.')[1]]-i-3)]
                    cmd = cmd.lower()
                hexa.append(val(cmd, prm))
        except Exception as e:
            parm.log(e)
            hexa.append("0000")

    if compare:
        return hexa, instructions
    with open("out.bin","w") as file: return file.write("v2.0 raw\n" + " ".join(hexa))

## ===== TESTS ===== ##
def run_tests(file, compare):
    hexa, instructions = compile_file(file, True)
    n = 0
    with open(compare) as file:
        comp_hexa = file.read().split('\n')[1].split(' ')
    try:
        instructions = [e for e in instructions if e[0] != "." and len(e) > 1 and e[0] != "@"]
        for i in range(len(hexa)):
            if hexa[i] == comp_hexa[i]:
                n += 1
            else: parm.log(f"échec du test {i}, commande : \"{instructions[i]}\", sortie obtenue \"{hexa[i]}\", sortie attendue \"{comp_hexa[i]}\"")
    except:
        parm.log(f'\n{n} tests réussis sur {len(instructions)}')
    return n, len(instructions)

print("=== TESTS ===")
def commande(texte):
    cmd, prm = texte.split('\t')
    prm = [clean(e) for e in prm.split(',')]
    return val(clean(cmd), prm)

import os
p, t = 0, 0
chrono = time()
for folder in os.listdir("test_integration"):
    for file in os.listdir(f"test_integration/{folder}"):
        if file.split('.')[1] == "s":
            #print(f"\n\nTest fichier test_integration/{folder}/{file.split('.')[0]}")
            r = run_tests(f"test_integration/{folder}/{file}", compare = f"test_integration/{folder}/{file.replace('.s','.bin')}")
            p += r[0]
            t += r[1]
fin = time()
print(f'\n{p} tests réussis sur {t} en {int((fin-chrono)*1000)} ms')


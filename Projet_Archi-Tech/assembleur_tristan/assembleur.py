from PARM_utils import parm, clean

class assembleur:
    def __init__(self, inp = "PARMin.txt", out = "PARMout.bin", bavard = False):
        self.inp = inp
        self.out = out
        self.parm = parm(bavard = bavard)

    def b(self, n:int, l:int = 3)->str:
        b = bin(int(n) & 2**l-1)[2:]
        return str(int(int(n)<0))*(l-len(b)) + b

    def d(self, n:str, m:int = 16) -> int:
        if len(n) > m:
            return -1
        return int(n, 2)

    def val(self, cmd:str, prm:list)->hex:
        bit = 16
        if cmd in ["str","ldr"] and len(prm)==2: prm.insert(1,"#0")
        if cmd in ["muls","rsbs"]: prm = prm[:-1]
        
        total = self.parm.commandes[len(prm)][cmd]
        bit -= len(total)
        if cmd == "cmp" and prm[1][0] == "#":
            total = "00101"
            bit = 11
            prm = prm[::-1]
        if cmd == "movs" and prm[0][0] == "r" and prm[1][0] == "r":
            total = "00000"
            bit = 11
            cmd = "lsls"
            prm += ["#0"]
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

        for e in prs:
            if e[1] == -1:
                total += self.b(int(e[0])/div,bit-taille)
            else:
                total += self.b(e[0],e[1])
                taille -= e[1]
                bit -= e[1]
        retour = hex(self.d(total))[2:].zfill(4)
        return retour
    
    def compile(self, instructions = ""):
        self.parm.log('début de la compilation')
        n, hexa, branchs = 0, [], {}
        for i in instructions:
            if len(i) > 1 and i[0] == ".":
                branchs[i.split(".")[1].split(':')[0]] = n
            else:
                n += 1

        instructions = [i for i in instructions if len(i)>0 and i[0] != "."]
        for i in range(len(instructions)):
            instruction = instructions[i]
            self.parm.log('Instruction ' + instruction)
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
                    valeur = self.val(cmd, prm)
                    self.parm.log(f"hexa append {cmd} {prm}\t>{valeur}<")
                    hexa.append(valeur)
            except Exception as ex:
                self.parm.log(f'Erreur de compilation :\n{ex}\n====')
                hexa.append("0000")

        with open(self.out,"w") as file:
            return file.write("v2.0 raw\n" + " ".join(hexa))
        
    def compile_from_file(self, file = None):
        if not file:
            self.parm.log('Fichier par défaut')
            file = self.inp
        self.parm.log('Ouverture du fichier ' + file)
        with open(file,"r") as file:
            instructions = [i for i in file.read().split('\n') if len(i) > 1 and i[0] != "@"]
        self.compile(instructions)

    def compile_from_clang(self, file = "assembleurOUT.s"):
        if not file:
            self.parm.log('Fichier par défaut')
            file = self.input
        self.parm.log('Ouverture du fichier généré par Clang ' + file)
        with open(file,"r") as file:
            lignes = file.read().split("run:\n")[1].split(".Lfunc_end0:")[0].split('\n')[5:]
        instructions = [i.strip().lower() for i in lignes if len(i) > 1 and i.strip()[0] != "@"]# and not "LBB" in i]
        self.compile(instructions)

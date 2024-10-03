from assembleur import assembleur

assembleur = assembleur()
print(assembleur.val("ldr", ["r1", "sp", "#68"]))

assembleur.out = "out.bin"
assembleur.compile(["ldr r1, [sp, #68]"])
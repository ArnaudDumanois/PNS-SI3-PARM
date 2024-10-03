lsls   	r2, r0, #31
lsls	r7, r2, #0
lsrs	r2, r0, #31
lsrs	r7, r2, #0
asrs	r2, r0, #31
asrs	r2, r7, #0
adds	r2, r7, r0
adds	r2, r3, r7
subs	r2, r7, r0
subs	r2, r3, r7
adds	r2, r7, #0
adds	r7, r4, #7
subs	r2, r7, #0
subs	r7, r4, #7
movs	r0, #1
movs	r7, #255
ands	r5, r2
ands	r4, r7
eors	r1, r6
eors	r6, r6
lsls	r7, r1
lsls	r7, r4
lsrs	r4, r0
lsrs	r3, r7
asrs	r2, r7
asrs	r7, r0
adcs	r6, r5
adcs	r2, r0
sbcs	r0, r1
sbcs	r4, r2
rors	r7, r3
rors	r5, r6
tst	r2, r7
tst	r3, r3
rsbs	r4, r6, #0
rsbs	r1, r0, #0
cmp	r1, r2
cmp	r0, r0
cmn	r5, r6
cmn	r1, r6
orrs	r3, r7
orrs	r1, r7
muls	r2, r0, r2
muls	r6, r4, r6
bics	r5, r2
bics	r6, r3
mvns	r7, r7
mvns	r2, r3
str	r0, [sp, #16]
str	r5, [sp, #464]
ldr	r0, [sp, #16]
ldr	r5, [sp, #464]
add	sp, #28
add	sp, #476
sub	sp, #28
sub	sp, #476
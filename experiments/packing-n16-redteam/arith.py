from decimal import Decimal as D, getcontext
getcontext().prec = 40
def sqrt(x): return D(x).sqrt()
def mpf(x): return D(str(x))
pi = D("3.141592653589793238462643383279502884197")
r3 = sqrt(3)

def a_from_budget(B):   # (sqrt3/4) a^2 = B
    return sqrt(4*B/r3)

print("== the four headline numbers ==")
print("Oler   a16 >= (-3+sqrt129)/2 =", (-3+sqrt(129))/2)
print("       s16 >= 2*that + 2sqrt3 =", 2*((-3+sqrt(129))/2)+2*r3, "  (repo: 11.821918)")
print("record a16 >= 1+2sqrt3       =", 1+2*r3)
print("       s16 >= 2+6sqrt3       =", 2+6*r3, "  (repo: 12.392304845413264)")
print("upper  s16 <= 12.713629 -> a16 <=", (mpf('12.713629')-2*r3)/2, " (repo 4.6247636)")
print("       G-L d(16)=0.216227269309782 -> a =", 1/mpf('0.216227269309782'))
print("       -> s =", 2/mpf('0.216227269309782')+2*r3)
print()
print("== area ceilings ==")
print("U0 15*pi/4          -> a <=", a_from_budget(15*pi/4), " (limit: 5.216032)")
print("U1 3*pi/6+12*pi/4   -> a <=", a_from_budget(pi/2+3*pi), " (limit: 5.039166 / shapes 5.0391657)")
print("hex 15*3sqrt3/8     -> a <=", a_from_budget(15*3*r3/8), " (limit: 4.743416)")
print("3*pi/6+12*3sqrt3/8  = ", pi/2+12*3*r3/8)
print("   -> a <=", a_from_budget(pi/2+12*3*r3/8), "   *** n16-dual states 4.65194 ***")
print("   what cap gives 4.65194? ", (r3/4*mpf('4.65194')**2 - pi/2)/12)
print("15*A6 (A6=0.674981) -> a <=", a_from_budget(15*mpf('0.674981')), " (limit: 4.835498)")
print("3*pi/6+12*A6        -> a <=", a_from_budget(pi/2+12*mpf('0.674981')), " (limit X2: 4.725804)")
print()
print("== area(T_a) checks ==")
for a in ('4.6247636','4.464101615137754','4.46335'):
    print(f"  a={a}: area = {r3/4*mpf(a)**2}")
print("  15*3sqrt3/8 =", 15*3*r3/8, "  deficit vs a=4.6247636:", 15*3*r3/8 - r3/4*mpf('4.6247636')**2)
print("  3*(3sqrt3/8 - pi/6) =", 3*(3*r3/8-pi/6))
print()
print("== f(1) and the Reuleaux claim ==")
print("f(1) = pi/3 - sqrt3/4      =", pi/3-r3/4)
print("3sqrt3/8                   =", 3*r3/8)
print("(pi-sqrt3)/2 (Reuleaux)    =", (pi-r3)/2)
print("pi/4                       =", pi/4)
print()
print("== headroom nit (verification-2 D3) ==")
print("4.6247636 - 446335/99998 =", mpf('4.6247636')-mpf(446335)/99998)
print("4.6247636 - (1+2sqrt3)   =", mpf('4.6247636')-(1+2*r3))
print()
print("== rational bounds vs 1+2sqrt3 ==")
for label,num,den in (("n16-covering banner",139503175473,31250000000),
                      ("cert_rational.json",446410161513599,10**14),
                      ("n16-dual",2232048569,500000000),
                      ("n16-shapes",4463841021,10**9),
                      ("n16-covering (dilated)",446335,99998)):
    v = mpf(num)/den
    print(f"  {label:24s} {v}  below 1+2sqrt3? {v < 1+2*r3}")

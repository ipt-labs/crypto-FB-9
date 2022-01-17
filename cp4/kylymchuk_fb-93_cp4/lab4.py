import random
min=2**255+1
max=2**256-1

def getp():
    while True:
        p=random.randrange(min, max, 2)
        if p%3==0 or p%5==0 or p%7==0 or p%11==0 or p%13==0:
            continue
        d, s = ds(p)
        if miller_rabin(p, d, s):
            return p

def miller_rabin(p, d, s):
    for i in range(0, 5):
        x=random.randrange(17, p, 2)
        if gcd(x,p) != 1: return 0
        mark=True
        num = pow(x,d,p)
        if num == 1 or num-p == -1: prime = 1
        else:
            for r in range(1, s):
                num = pow(num,2,p)
                if num - p == -1:
                    mark=False
                    break
                elif num == 1: return 0
        if mark: return 0
    return 1 

def ds(p):
    d = p-1
    s = 0
    while(d%2 == 0):
        d = d//2
        s +=1
    return d,s

def euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = euclid(b, a % b)
        return d, y, x - y * (a // b)

def reverse(a, b):
    x = euclid(a, b)[1]
    return x % b

def gcd(a, b):
    while a > 0 and b > 0:
        if a > b: a %= b
        else: b %= a
    return a + b

def gen_pq():
    while True:
        p1=getp()
        q1=getp()
        p2=getp()
        q2=getp()
        if p1!=q1 and p1!=p2 and p1!=q2 and q1!=q2 and q1!=p2 and p2!=q2:
            if q1*p1<=p2*q2:
                return p1, q1, p2, q2
            else:
                return p2, q2, p1, q1

#p1, q1, p2, q2 = gen_pq()

def gen_key(p, q):
    fn=(p-1)*(q-1)
    n=p*q
    while True:
        e=random.randrange(2, fn)
        if gcd(e, fn) == 1:
            break
    d=reverse(e, fn)
    return [d, p, q], [n, e]

#d1, n1 = gen_key(p1, q1)
#d2, n2 = gen_key(p2, q2)

def encrypt(m, e, n):
    return pow(m, e, n)

def decrypt(c, d, n):
    return pow(c, d, n)

def sign(m, d, n):
    return pow(m, d, n)

def verify(s, e, n, m):
    return pow(s, e, n) == m

#def sendkey():
#def receivekey():

#локальна переписка
m=65166659943491513276856648397150629050020985208127901655491569854081304258961
p1=61243515839170765062248483224368043173433601463612354184187057703427791701081
q1=69601466102931450588341025905410714147007252475248556046943745068877855632929
p2=107609762294470384737527317232869430366679331862432513400678784912787201186833
q2=92157630482613438383463816444422199356328642252664006652348314870248007698701
d1, op1 = gen_key(p1, q1)
d2, op2 = gen_key(p2, q2)
#Для Аліси
cyfrAlica=encrypt(m, op2[1], op2[0])
print("Шифрований текст:", cyfrAlica)

text=decrypt(cyfrAlica, d2[0], op2[0])
print("Відкритий текст:", text)

s=sign(m, d1[0], op1[0])
print(s)
t=verify(s, op1[1], op1[0], m)
print(t)

#Для Боба
cyfrBob=encrypt(m, op1[1], op1[0])
print("Шифрований текст:", cyfrBob)

text=decrypt(cyfrBob, d1[0], op1[0])
print("Відкритий текст:", text)

s=sign(m, d2[0], op2[0])
print(s)
t=verify(s, op2[1], op2[0], m)
print(t)




#site
modulus="84658513BFDC44D3F66B560A2AB2D33B0637D0752D9CFC077CD440A35D7487F9"
exp="10001"


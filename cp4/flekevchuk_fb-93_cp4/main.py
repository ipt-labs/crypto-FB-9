from random import randint

toNumber = lambda text: int(text.encode().hex(), 16)
toString = lambda number: bytearray.fromhex(hex(number)[2:]).decode()



MR_ITERATIONS = 5
KEY_LENGTH = 256
MAX_KEY = pow(2, KEY_LENGTH) -1
MIN_KEY = pow(2, KEY_LENGTH -1)

fi = lambda p , q: (p-1)*(q-1)

def GCD(a,b):
  arr = []
  while a>0 and b>0:
    if a>b:
      arr.append(-(a//b))
      a %=b
    else :
      arr.append(-(b//a))
      b %=a
  return [arr, a + b]

def sum(arr):
  q1 = 0
  q2 = 1
  for q in arr:
    temp = q2
    q2 = q2 * q + q1
    q1 = temp
  return q1 

def revers(a, mod): 
  payload = GCD(a, mod) 
  rev = sum(payload[0])
  if rev > 0 :
    return [rev, payload[1]]
  return [rev + mod,  payload[1]]

def quick_pow(a, b, m):
    ab = 1
    while b > 0:
        if b & 1:
            ab = (ab * a) % m
        b >>= 1
        a = (a ** 2) % m
    return ab


def splitP(p):
    s = 0
    d = p - 1
    while d%2 == 0:
        d>>=1
        s+=1
    return (d, s)

def MRPrimeTest(p, s, d, exp):
    expPow = quick_pow(exp, d, p) 
    if expPow == 1 or expPow == p-1:
        return True
    rRange = range(1,s)
    for r in rRange:
        expPow = quick_pow(expPow, 2, p)
        if expPow == p - 1:
            return True
        if expPow == 1:
            return False




def MRTest(p):
    d, s = splitP(p)
    if not(MRPrimeTest(p, s, d, 2)) or not(MRPrimeTest(p, s, d, 3)) or not(MRPrimeTest(p, s, d, 5)) or not(MRPrimeTest(p, s, d, 7)):
        return False
    k = 0
    while k < MR_ITERATIONS:
        exp = randint(2, p-1)
        if GCD(exp,p)[1] > 1 or not MRPrimeTest(p, s, d, exp):
            return False
        k+=1
    return True

def generetePrime():
    p = randint(MIN_KEY, MAX_KEY)
    if not p & 1:
        p += 1
    nRange = range(p, MAX_KEY, 2)
    for n in nRange: 
        if MRTest(n):
            return n

def generetED(fn):
    e = randint(2, fn - 1)
    gcd = revers(e, fn)
    while gcd[1] > 1:
        e = randint(2, fn - 1)
        gcd = revers(e, fn)
    return (e, gcd[0])

def genereteKEYS():
    p = generetePrime()
    q = generetePrime()
    while p == q:
        q = generetePrime()
    n = p * q
    fn = fi(p,q)
    e, d = generetED(fn)
    return (n, e, d)

class User:
    def __init__(self, name, privateKey, n, RSAServer):
        self.__privateKey = privateKey
        self.module = n 
        self.name = name
        self.RSAServer = RSAServer
        self.__keys = dict()

    def encrypt(self, mesage, name):
        e, n = self.RSAServer.openKeys[name]
        return quick_pow(mesage, e ,n)

    def decrypt(self, cmesage):
        return quick_pow(cmesage, self.__privateKey , self.module)

    def sign(self, mesage):
        return (mesage, self.decrypt(mesage))
    
    def verify(self, dataVerify, name):
        return dataVerify[0] == self.encrypt(dataVerify[1], name)

    def sendKey(self, name):
        if self.module < self.RSAServer.openKeys[name][1]:
            self.setNewKeys(self.RSAServer.openKeys[name][1])
            print('chenged')
        k = randint(2, self.module - 1)
        kde = self.encrypt(self.decrypt(k), name)
        ke = self.encrypt(k, name)
        return (self.name, ke, kde)

    def receiveKey(self,keyInfo):
        name, ke, kde = keyInfo  
        k = self.decrypt(ke)
        kd = self.decrypt(kde)
        toVerify = (k,kd)
        if self.verify(toVerify, name):
            self.__keys[name] = k
            print('key received',k)
        else:
            print('error occurred')

    def setNewKeys(self, n1):
        n, e, d = genereteKEYS()
        while n < n1:
            n, e, d = genereteKEYS()
        self.module , self.__privateKey = (n, d)
        self.RSAServer.setNewKeysByUN(self.name, e, n)   

class RSAma:
    openKeys = None
    def __init__(self):
        if(self.openKeys):
            return self
        self.openKeys = {
            "test": (0x10001, 0xC51B6DE4CCC1023B5D9D5021D21D3AB393BA806E04AB610C1989A7F4FA873575)
        }
    
    def addUser(self, name):
        n, e, d = genereteKEYS()
        user = User(name, d, n, self)
        self.openKeys[name] = (e,n)
        return user
    
    def setNewKeysByUN(self, name, e ,n):
        self.openKeys[name] = (e,n)


RSA_SERVER = RSAma()
Alice = RSA_SERVER.addUser("Alice")
Bob = RSA_SERVER.addUser("Bob")

Alice.receiveKey(
    Bob.sendKey(Alice.name)
    )

'''

print(Alice.verify(
    Bob.sign(1111), Bob.name
    )
)


print(toString(
    Alice.decrypt(
        Bob.encrypt(
            toNumber("test message"),Alice.name
            )
        )
    )
)

'''




'''
print(Bob.verify((toNumber("test message"),0x3B763D4A8336C1613E39297A964D98205B266B11DCC2F5248FDF855474668862), "test"))

print([str(hex(i)).upper()[2:] for i in RSA_SERVER.openKeys["Bob"]])
print(str(hex(Bob.sign(toNumber('test message'))[1])).upper()[2:])

print([str(hex(i)).upper()[2:] for i in RSA_SERVER.openKeys["Bob"]])
A = int(input())
print(Bob.decrypt(A))


print(str(hex(Bob.encrypt("test message", "test"))).upper()[2:])

Alice = RSA_SERVER.addUser("Alice")
Bob = RSA_SERVER.addUser("Bob")

k = Bob.sendKey(Alice.name)

Alice.receiveKey(k)

'''



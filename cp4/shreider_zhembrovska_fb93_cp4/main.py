import random
interval = [1+2**255, -1+2**256]

def gcd(a, b):
    while a != 0 and b != 0:
        if a > b: a = a % b
        else: b = b % a
    return a + b

def inverse(a, n):
    q = [0, 1]
    while a != 0 and n != 0:
        if a > n:
            q.append(a // n); a = a % n
        else:
            q.append(n // a); n = n % a
    for i in range(2, len(q)): q[i] = q[i - 2] - q[i] * q[i - 1]
    return q[-2]

def gorner(x,e,m):
    e, y = bin(e), 1
    for i in e[2:]:
        y = (y ** 2) % m
        y = (y*x**int(i))%m
    return y

def get_prime():
    x = random.randint(interval[0], interval[1])
    m0 = x if x%2 != 0 else x+1
    for i in range(m0, interval[1], 2):
        if(is_prime(i)) == 1: return i
    return get_prime()

def is_prime(p):
    if(p%3 == 0 or p%5 == 0 or p%7 == 0): return 0
    else: return miller_rabin(p)

def ds(p):
    d,s = p-1,0
    while(d%2 == 0):
        d = d//2
        s +=1
    return d,s

def miller_rabin(p):
    d,s = ds(p)
    for i in range(20):
        prime = 0
        x = random.randint(1,p)
        if gcd(x,p) != 1: return 0
        num = gorner(x,d,p)
        if num == 1 or num-p == -1: prime = 1
        else:
            for r in range(1, s):
                num = gorner(num,2,p)
                if num - p == -1:
                    prime = 1
                    break
                elif num == 1: return 0
        if not prime: return 0
    return 1

def gen_keys():
    p, q = get_prime(), get_prime()
    while p == q:
        p = get_prime()
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(2,phi-1)
    while(gcd(e,phi) != 1): e = random.randint(2,phi-1)
    d = inverse(e,phi)%phi
    return (e,n,d)

class Node:
    def __init__(self):
        self.e = 0
        self.n = 0
        self.d = 0

    def GenerateKeyPair(self,n):
        self.e, self.n, self.d = gen_keys()
        while self.n < n:
            self.e, self.n, self.d = gen_keys()

    def Encrypt(self, data, e, n):
        return gorner(data, e, n)

    def Decrypt(self, data, d, n):
        return gorner(data, d, n)

    def Sign(self, data):
        return gorner(data, self.d, self.n)

    def Verify(self,data,sign,e,n):
        return gorner(sign,e,n) == data

    def SendKey(self,data,e,n):
        data1 = self.Encrypt(data,e,n)
        sign = self.Sign(data)
        sign1 = self.Encrypt(sign,e,n)
        return (data1,sign1)

    def ReceiveKey(self,pack,e,n):
        data = self.Encrypt(pack[0],self.d,self.n)
        sign = self.Decrypt(pack[1],self.d,self.n)
        if (self.Verify(data,sign,e,n) == False):
            print('Verification failed')
        else: return data

    def PrintKeys(self):
        print('e', self.e)
        print('n', self.n)
        print('d', self.d)

def check():
    A = Node()
    server_n = int(0x9A8EE5B763FF0B0570C5B41AFD881FFEFD28757C68CB291E18D4042001987081447A86BDD7EA57F8722308B5ECB695F1B8B57702331C834EA76773224FA51693)
    server_e = int(0x10001)

    #генеруємо ключі, які будемо використовувати нижче
    #A.GenerateKeyPair(server_n)
    #A.PrintKeys()

    A.e = 10852746501111419120795960929289968488613208275606288276151660071245230394717794773237389989976950293838562598240507342259497868077712481899388858960780149
    A.n = 11729174846780466515621400509184851154650274595662807386553577455135392784735642578294635291713690950972273380803161955115964315406336833363293791988506049
    A.d = 10395809668393900846290703319055430003363574478006090934093666592738743330019249614087926613845539922756948307649748442660101450656799819642150514339729889
    print('\nmy keys')
    print('e ', hex(A.e)[2:], '\nn ', hex(A.n)[2:], '\nd ', hex(A.d)[2:])

    msg = 114888933979642393893806692060425606139553765450567466106219951259984737489665
    print('\nmsg ', hex(msg)[2:])

    print('\n-encrypt here with server keys, decrypt on the server-')
    print('encrypted msg', hex(A.Encrypt(msg,server_e,server_n))[2:])

    print('\n-encrypt on the server with my keys, decrypt here-')
    emsg = 0xD6A64F78722422EAB4E0AC03BFEB8029ACF0CB50C929BF05D09C707BC22F7C768EE7D50197CF0C7B2017EAE1E393506BD807D5D037FF57DB909120659FF3ADA9
    print('encrypted msg ', emsg)
    print('decrypted msg ', hex(A.Decrypt(emsg,A.d,A.n))[2:])

    print('\n-create a sign here and verify on the server-')
    print('my sign ', hex(A.Sign(msg))[2:])

    print('\n-create a sign on the server and verify on the here-')
    server_sign = 0x2A777F1355107E54D60F3C9B1EEEA89489DFCB5E88CB99A85F42C025C086D90B86CEDD6E77E209772D211AB4876B31F4AB17DDA9266EB3CED5E1618F14269335
    print('server sign ', server_sign)
    print(A.Verify(msg,int(server_sign),server_e,server_n))

def protocol():
    Mabel = Node()
    Dipper = Node()

    Dipper.GenerateKeyPair(0)
    Mabel.GenerateKeyPair(Mabel.n)

    print('\nMabel keys')
    Mabel.PrintKeys()
    print('\nDipper keys')
    Dipper.PrintKeys()

    k = random.randint(0, 2**256)
    print('\nkey', k)
    pack = Mabel.SendKey(k,Dipper.e,Dipper.n)
    print('Mabel send ', pack)
    result = Dipper.ReceiveKey(pack,Mabel.e,Mabel.n)
    print('Dipper receive', result)

protocol()
import random
from math import gcd

def toHex(text):
  text = text.encode('utf-8')
  sms = int(text.hex(), 16)
  return sms

def toText(sms):
  text = bytes.fromhex(hex(sms)[2:]).decode('ASCII')
  return text
  
def int_to_hex(number):
    return hex(number)[2:].upper()

def hex_to_int(hex_value):
    return int(hex_value, 16)

def miller_rabin(n, k = 100):

    primes = [2, 3, 5, 7, 11]
    r = 0
    s = n-1

    if n == 2 :
        return True
    
    if 0 in list(map(lambda x: n%x, primes)):
       return False 
    
    while s % 2 == 0:
        r += 1
        s //= 2

    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            
            return False
    return True
  
def randomPrime(min=pow(2, 255)+1, max=pow(2, 256)-1):
  p = random.randrange(min, max)
  #print(p, 'random num')
  while not miller_rabin(p):
   p = random.randrange(min, max)
  return p

def pANDq():
  p, q = randomPrime(), randomPrime()
  p1, q1 = randomPrime(), randomPrime()
  while p*q > p1*q1:
      p, q = randomPrime(), randomPrime()
  return (p, q, p1, q1)
      
def RSA(p, q):
  #p, q = pANDq()
  Eiler = (p-1)*(q-1)
  n = p*q
  e = random.randrange(2, Eiler)
  while gcd(e, Eiler) != 1:
    e = random.randrange(2, Eiler)
  d = pow(e, -1, Eiler)
  privateKey = (d, p, q)
  openKey = (n, e)
  return privateKey, openKey

def Encryption(sms, n, e):
  return pow(sms, e, n)

def Decryption(encSms, d, p, q):
  return pow(encSms, d, p*q)

def Signature(sms, d, p, q):
  return pow(sms, d, p*q)

def SignVerify(sms, sign, openKey):
  n, e = openKey
  if pow(sign, e, n) == sms: return True
  else: return False

def sendMessage(sms, openKey, privateKey):
  n, e = openKey
  d, p, q = privateKey
  encryptSms = Encryption(sms, n, e)
  sign = Signature(sms, d, p, q)
  return encryptSms, sign

def recieveMessage(encryptSms, sign, openKey, privateKey):
  n, e = openKey
  d, p, q = privateKey
  sms = Decryption(encryptSms, d, p, q)
  if SignVerify(sms, sign, openKey): return sms
  else: return 1


text = "Passed exams - happy holidays!"
print('Message: ',  text)
sms = toHex(text)
p, q, p1, q1 = pANDq()
A = RSA(p, q)
B = RSA(p1, q1)
encryptSms, sign = sendMessage(sms, B[1], A[0])
print(encryptSms,'\n', sign, 'SEND SUCCESSFUL\n')
sms = recieveMessage(encryptSms, sign, A[1], B[0])
print(sms, 'RECIEVED')
text = toText(sms)
print(text, "Message that we have recieved")
def test():
 modulus =  'C362672A074156E3BC5D9882C0A8B40C49EA95F021994276B58A57EA715AD551'
 exp = '10001'
 
 p, q, p1, q1 = pANDq()
 #A = RSA(p, q)
 privateKey, openKey = RSA(p, q)
 e, m = int_to_hex(openKey[1]),int_to_hex(openKey[0])
 encrypted = Encryption(sms, openKey[0], openKey[1])
 modulus, exp = hex_to_int(modulus), hex_to_int(exp)
 print('Message: ', text)
 print('n = ', m)
 print('e = ', e)
 print('Encrypted: ', int_to_hex(Encryption(sms, openKey[0], openKey[1])))


#test()
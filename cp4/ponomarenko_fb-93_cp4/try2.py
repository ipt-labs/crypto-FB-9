def Encrypt(M, e, n):
	C = pow(M,e,n)
	print("C=",M,"^",e,"mod",n)
	return C

def Decrypt(C, d, n):
	M = pow(C,d,n)
	print("M=",C,"^",d,"mod",n)
	return M

def Sign(M, d, n):
	S = pow(M, d, n)
	print("S=",M,"^",d,"mod",n)
	return S

def Verify(S, e, n):
	M = pow(S, e, n)
	print("M=",S,"^",e,"mod",n)
	return M

def encode(string):
    return int(string.encode().hex(), 16)
def decode(int):
    return bytearray.fromhex(hex(int)[2:]).decode()
def int_to_hex(int):
    return hex(int)[2:].upper()

def hex_to_int(hex):
    return int(hex, 16)

n = "B85763FAB059D354A494CFB77497A763F7F71ABD589FC41943DF220F5CA0AF83DF653BF880EB7F545E2F0A5DA1DEAE4EB81EFE9EB74D834A58E7BC22C1E7A400D763"
n = hex_to_int(n)
print("n:", n)
e = "10001"
e = hex_to_int(e)
print("e:",e)
M = encode(input("Enter your message: "))
C = Encrypt(M, e, n)
C = int_to_hex(C)
print("C=",C)

n1 = 3743229692300665959918822428946270639860501351726619833815616983579413746253716482896410415879632836939647544180052474993673765580605284254596922528777287860263
n_hex = int_to_hex(n1)
print("n_hex:",n_hex)
e1 = 2243354844171827904141908533598054827684957610696113515644157327440866424240202428781126753144277966556869874952481832015964821594484683776958030037002118509767
e_hex = int_to_hex(e1)
print("e_hex:",e_hex)
d1 = 1201953083881308353509259973048105275335878291167660015261370926490480022800841262763816423707588656300000172862928876675155985061871540154811492604641129991463
C_encrypted = "0166C3260D8FA65DB27B16233E5DECADBED421B3D93DD6F9F4AF6CC8FCAEE991B456DE8E32D4705A9FA28FFC1F051574F67C34BAA88879AC3B2C2C08EB6E3A7C4D1376"
C_encrypted = hex_to_int(C_encrypted)
M_decrypted = Decrypt(C_encrypted, d1, n1)
M_decrypted = decode(M_decrypted)
print("M=",M_decrypted)

S = Sign(M,d1,n1)
S = int_to_hex(S)
print("S=",S)

S1 = "129729A11F3063CA180F478C59DE04A1209C3B9CD1C02B062F9D7E0D9EB4D5A9A6AF2198C7E9A149DEEB21DBF23C2BA87FB1BD59F692154B0EF5CBDC50EB1C769B7F"
S1 = hex_to_int(S1)
V = Verify(S1,e,n)
V = decode(V)
print("V=",V)
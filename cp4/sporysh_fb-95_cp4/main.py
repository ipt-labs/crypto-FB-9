import LAB4_my_rsa

if __name__ == '__main__':
    L4 = LAB4_my_rsa.my_rsa(4, 256)
    print("Working with remote server")
    print("We encrypt, server dercrypts")
    L4.Decrypt()
    print("server signs")
    L4.Sign()
    print("server encrypts")
    L4.Encrypt()
    print("server verifies")
    L4.Verify()
    print("Receive key")
    L4.ReceiveKey()
    print("Send  key")
    L4.SendKey()

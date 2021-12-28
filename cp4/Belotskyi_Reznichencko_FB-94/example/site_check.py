from main_RSA import *

site_n_hex = "E2DBC75C336AA7F896CF5107099DBBE08577875824A2628C8D282F0F66F620790F540F52953FA301FC0EF8DD76ADFDE420BA723B0227532F2F03BCAB6779ADA70C4368805510B5EF6306886B626FA0F1D84B6040349223E731B055D27D05FF16C37A9A9FE71E8EF2C22098F27BA560D6D17F0E31D399423D4E4ECE7C571C8D5D"
site_e_hex = "10001"

site_n = int(site_n_hex, 16)
site_e = int(site_e_hex, 16)
print(f"n from site: {site_n}")
print(f"e from site: {site_e}")

Alice = algorithm_RSA("Alice", 64)
Alice.generate_primitive_numbers_pair()
Alice.make_crypto_RSA()
Alice.show_info()

k = random.randint(1, Alice.n)
print(f"{Alice.name} choose message k: {k}")
k1_S1 = Alice.SendKey(k, site_e, site_n)
print(f"{Alice.name} send message (k1, S1): ({k1_S1[0]}, {k1_S1[1]})")
print(f"{Alice.name} send message (k1, S1) in hex: ({hex(k1_S1[0])}, {hex(k1_S1[1])})")
print(f"{Alice.name} n in hex: {hex(Alice.n)}")
print(f"{Alice.name} e in hex: {hex(Alice.e)}")
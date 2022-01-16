import affine_cypher_tools as af
import sys
sys.path.insert(0, '../../cp1/Denysiuk_fb-93_tovstonojenko_fb-93_cp1')
import my_lib

text=my_lib.filter_text('../../tasks/cp3/variants.utf8/04.txt', False)
supposable_keys = af.attack_on_cypher(text)
decrypted_text=''
for i in supposable_keys:
    b = af.decrypt_text(text, i)
    if af.validation(b):
        decrypted_text=b
        print(f'Supposable key:{i}')
        print(b, '\n')

if decrypted_text!='':
    with open('./decrypted_text.txt', mode='w', encoding='utf8') as f:
        f.write(decrypted_text)
    print('The text has been written to the file')



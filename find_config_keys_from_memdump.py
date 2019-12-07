# Script to find the AES Key & IV required to decrypt a configuration backup created from Huawei HG6xx series routers
# https://hg659.home.blog/
# https://github.com/jameskeenan295/huawei_router_aes_keys
# Requires two files as input:
# 1) a memory dump from the router running the version of firmware from which the config backup was created
#    dd if=/dev/mem of=/mnt/usbpath/mem.dump bs=1024
# 2) the encrypted config backup file
# adjust file names for those two in the fname variables below.
# For help with getting dd to work on the router (because it is not included in the default firmware), see the blog above
# usage: python3 ./find_config_keys_from_memdump.py

import re, zlib
from binascii import hexlify 
from Crypto.Cipher import AES

def test_decrypt_key(encrypted_config_data, AES256CBC_IV, AES256CBC_KEY):
    cipher = AES.new(AES256CBC_KEY, AES.MODE_CBC, AES256CBC_IV)
    try:
        decrypted_data = cipher.decrypt(encrypted_config_data)
        zlib.decompress(decrypted_data)
        return True # if we get to here without exception, then we've found the right IV & KEY!
    except:
        return False # zlib decompress failed so we havent found the right key
    

def get_keys_from_memdump(): 
    ## Read the memdump file, then close it
    memdump_fname = 'memorydump.dump' # adjust file name here...
    memdump_f = open(memdump_fname , 'rb')
    memdump_data = memdump_f.read()
    memdump_f.close()
    
    regex_pattern = b'\x00\x00\x00\x00\xff\xff\xff\xd8([\x00-\xff]{32})\x00\x00\x00\x00' # Huawei AES keys & IV's have consistent start & end delimiters in memory, so we can find them all quickly with a simple regex!
    
    possible_keys = re.findall(regex_pattern, memdump_data)
    key_list = []
    for possible_key in possible_keys:
        if(possible_key not in key_list): key_list.append(possible_key)
    return key_list

def test_keys():
    encrypted_config_fname = 'configsave.conf'
    encrypted_config_f = open(encrypted_config_fname , 'rb')
    encrypted_config_data = encrypted_config_f.read()
    encrypted_config_f.close()
    global key_list
    key_list = get_keys_from_memdump()
    print('Found', len(key_list), 'unique 256bit blobs of key material from memdump. Starting to test all possible combinations now')
    x = len(key_list) - 1
    y = len(key_list) - 1
    loopcount = 0
    while (x > 0):
        IV_temp = key_list[x] #test every IV
        AES256_IV_a = IV_temp[:16] # IV is only 128bit whereas key is 256bit, so we have to split it into a & b and try both
        AES256_IV_b = IV_temp[16:]
        while(y > 0):
            loopcount += 1
            AES256KEY = key_list[y] # test every key with every IV
            if(test_decrypt_key(encrypted_config_data, AES256_IV_a, AES256KEY)) :
                print('Found the right IV and key after testing', loopcount, 'combinations')
                print('key = ', str((hexlify(AES256KEY)),"utf-8"))
                print('iv = ', str((hexlify(AES256_IV_a)),"utf-8"))
                return True
            if(test_decrypt_key(encrypted_config_data, AES256_IV_b, AES256KEY)) :
                print('Found the right IV and key after testing', loopcount, 'combinations')
                print('key = ', str((hexlify(AES256KEY)),"utf-8"))
                print('iv = ', str((hexlify(AES256_IV_b)),"utf-8"))
                return True
            y -= 1
        y = len(key_list) - 1
        x -= 1
    print('Loopcount = ', loopcount)
    return False

key_list = []
test_keys()

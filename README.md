# huawei_router_aes_keys
Extract AES keys from huawei hg6xx routers for decrypting saved config files
See https://hg659.home.blog/ for the writeup
Requires python3. Was tested on kali2019.

Instructions:
Create a folder, and place these 3 things in there:
1) Your saved-config file from the router, called 'savedconfig.conf'
2) Memory dump from the router, called 'memorydump.dump'
3) find_config_keys_from_memdump.py

Usage:
python3 ./find_config_keys_from_memdump.py

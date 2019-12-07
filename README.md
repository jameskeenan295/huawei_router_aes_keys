# huawei_router_aes_keys
Extract AES keys from huawei hg6xx routers for decrypting saved config files
See https://hg659.home.blog/ for the writeup
Requires python3. Was tested on kali2019.

Instructions:
Create a folder, and place these 3 things in there:
Your saved-config file from the router
Memory dump from the router
This script

usage:
python3 ./find_config_keys_from_memdump.py

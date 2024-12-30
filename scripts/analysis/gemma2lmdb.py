#!/usr/bin/env python3


# Create vector database after addition of trait category and full description


import sys
import argparse
import json
import lmdb
from struct import *

parser = argparse.ArgumentParser(description='Turn GEMMA assoc output into an lmdb db.')
parser.add_argument('--db', default="../../processed_data/project.mdb", help="DB name")
parser.add_argument('--meta',required=False,help="JSON meta file name")
parser.add_argument('files',nargs='*', help="GEMMA file(s)")
args = parser.parse_args()

# ASCII
X=ord('X')
Y=ord('Y')

meta = { "type": "gemma-assoc",
         "version": 1.0,
         "key-format": ">cL",
         "rec-format": "=ffff" }
log = {} # track output log
hits = [] # track hits

with lmdb.open(args.db,subdir=False) as env:
    for fn in args.files:
        print(f"Processing {fn}...")
        if "log" in fn:
            with open(fn) as f:
                log[fn] = f.read()
        else:
            with open(fn) as f:
                with env.begin(write=True) as txn:
                    for line in f.readlines():
                        cont=line.rstrip('\n').split('\t')
                        chr,rs,pos,miss,a1,a0,af,beta,se,l_mle,p_lrt,desc,full_desc = line.rstrip('\n').split('\t')
                        if chr=='chr':
                            continue
                        if (chr =='X'):
                            chr = X
                        elif (chr =='Y'):
                            chr = Y
                        elif (chr=='-9'):
                            continue # ignore when chr=-9
                        else:
                            chr = int(chr)
                        chr_c = pack('c', bytes([chr]))
                        key = pack('>cLfff', chr_c, int(pos), float(se), float(l_mle), float(p_lrt))
                        val = pack('=fffffB100s', float(af), float(beta), float(se), float(l_mle), float(p_lrt), int(desc), bytes(full_desc, encoding='utf-8')) 
                        res = txn.put(key, bytes(val), dupdata=False, overwrite=False)
                        print('insertion return value is', res)
                        if res:
                            if float(p_lrt) > 2.0:
                                hits.append([chr, int(pos), rs, p_lrt])
                        else:
                             print(f"WARNING: failed to update lmdb record with key {key} -- probably a duplicate {chr}:{pos} ({test_chr_c}:{test_pos})")
    with env.begin() as txn:
        with txn.cursor() as curs:
            # quick check and output of keys
            for (key, val) in list(curs.iternext()):
                if key==b'meta':
                    continue
                else:
                    chr_c, pos, se, l_mle, p_lrt = unpack('>cLfff', key)
                    b_chr=unpack('c', chr_c)
                    chr=ord(b_chr)
                    #print('chromosome read is ', chr)
                    af, beta, se, l_mle, p_lrt, desc, b_full_desc= unpack('=fffffB100s', val)
                    full_desc=b_full_desc.decode('utf-8').strip('\x00')
                    #print('trait category read is ', desc)
                    #print('trait description read is ', full_desc)

    meta["hits"] = hits
    meta["log"] = log
    print("HELLO: ",file=sys.stderr)
    print(meta,file=sys.stderr)
    with env.begin(write=True) as txn:
        res = txn.put('meta'.encode(), json.dumps(meta).encode(), dupdata=False, overwrite=False)

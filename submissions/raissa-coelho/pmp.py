## Made By Raíssa Coelho

import argparse

def read_config(path):
    pmpcfg = []
    pmpaddr = []
    
    with open(path, "r") as file:
        for _ in range(4):
            pmpcfg.append(bin(int(file.readline().strip(), 16))[2:].zfill(8))
        
        for _ in range(4):
            pmpaddr.append(file.readline().strip())
            
    return pmpcfg, pmpaddr

def check_pmpcfg(pmcfg):
    L = pmcfg[0]
    A = pmcfg[3:5]
    X = pmcfg[5]
    W = pmcfg[6]
    R = pmcfg[7]
    
    return L, A, X, W, R

def pmp(pmpcfg, pmpaddr, physical_addr, mode, op):
    print("PMP Configuration:")
    physical_addr = int(physical_addr, 16)
    
    for i in range(4):
        cfg = pmpcfg[i]
        addr = [int(a, 16) for a in pmpaddr]
        L, A, X, W, R = check_pmpcfg(pmpcfg[i])

        #Lock
        if L == "1":
            print(f'PMP region {i} is locked\n')
            continue
        if A == "00":
            # OFF - Null region
            print(f'OFF - Null Region\n')
        if A == "01":
            # TOR - Top of range
            if i == 0:
                continue
            if addr[i - 1] <= physical_addr < addr[i]:
                if mode == "M":
                    print(f'Access granted.')
                elif mode == "S":
                    print(f'Acess granted.')
                elif mode == "U":
                    print(f'Acess granted.')
        if A == "10":
            # NA4 - Naturally aligned four-byte region
            print(f'NA4')
            if addr[i] <= physical_addr < addr[i] + 4:
                print(f'Physical address {physical_addr} is in the region {i}')
        if A == "11":
            # NAPOT - Naturally aligned power-of-two region
            print(f'NAPOT')
            napot = addr[i] & 0b111111111111
            size = 1 << (napot.bit_length())
            
            base = addr[i] & ~(size - 1)
            if base <= physical_addr < base + size:
                print(f'Physical address {hex(physical_addr)} is in the region {i}')  
        #print(f"  CFG{i}: {cfg} ADDR{i}: {addr} L: {L} A: {A} X: {X} W: {W} R: {R}")        

def main():
    parser = argparse.ArgumentParser(description='Verify acess.')
    
    parser.add_argument('path', type=str, help='pmp_configuration file')
    #parser.add_argument('addr', type=lambda x: int(x, 16), help='physical address in hexadecimal')
    parser.add_argument('addr', type=str, help='physical address in hexadecimal')
    parser.add_argument('mode', type=str, help='privilege mode')
    parser.add_argument('op', type=str, help='operation: read,write,execute/fetch')

    args = parser.parse_args()    
    pmpcfg, pmpaddr = read_config(args.path)
    
    #print(pmpcfg)
    #print(pmpaddr)
    
    pmp(pmpcfg, pmpaddr, args.addr, args.mode, args.op)
    
if __name__ == '__main__':
    main()
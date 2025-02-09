## Made By Raíssa Coelho

import argparse

"""read_config reads the PMP configuration file
    Args:
        path: path to the PMP configuration file
    Returns:
        pmpcfg: PMP configuration bits
"""
def read_config(path):
    pmpcfg = []
    pmpaddr = []
    
    with open(path, "r") as file:
        for _ in range(64):
            pmpcfg.append(bin(int(file.readline().strip(), 16))[2:].zfill(8))
        
        for _ in range(64):
            pmpaddr.append(file.readline().strip())
            
    return pmpcfg, pmpaddr


"""check_pmpcfg checks the PMP configuration bits
    Args:
        pmcfg: PMP configuration bits
    Returns:
        L: locked region
        A: address-matching mode
        X: execute permission
        W: write permission
        R: read permission
"""
def check_pmpcfg(pmcfg):
    L = pmcfg[0]
    A = pmcfg[3:5]
    X = pmcfg[5]
    W = pmcfg[6]
    R = pmcfg[7]
    
    return L, A, X, W, R

"""check_permission checks if the access is granted 
   or denied based on the mode and the permission bits
"""
def check_permission(mode, op, R, W, X):
    if mode == "M":
        print(f'Access granted.')
    elif mode == "S" or mode == "U":
        if op == "R" and R == "0":
            print(f'Access denied.')
        elif op == "W" and W == "0":
            print(f'Access denied.')
        elif op == "X" and X == "0":
            print(f'Access denied.')
        else:
            print(f'Access granted.')
                    
"""pmp checks the PMP configuration and address
    Args:
        pmpcfg: PMP configuration
        pmpaddr: PMP address
        physical_addr: physical address
        mode: privilege mode - M, S, U
        op: operation: read,write,execute - R, W, X
"""
def pmp(pmpcfg, pmpaddr, physical_addr, mode, op):
    physical_addr = int(physical_addr, 16)
    
    addr = [int(a, 16) for a in pmpaddr]
    for i in range(64):
        L, A, X, W, R = check_pmpcfg(pmpcfg[i])

        """ Locked region	
        """	
        if int(L) == 1:
            print(f'PMP region {i} is locked')
            continue
        
        """ Null region	
        """
        if A == "00":
            if mode == "M":
                print(f'Access granted.')
            else:
                print(f'Access denied.')
        
        """TOR - Top of range
            Args:
                addr: base address of the region
                physical_addr: physical address
        """
        if A == "01":
            if i == 0:
                continue
            if addr[i - 1] <= physical_addr < addr[i]:
                check_permission(mode, op, R, W, X)
            else:
                if mode == "M":
                    print(f'Access granted.')
                elif mode == "S" or mode == "U":
                    print(f'Access denied.')
        
        """NA4 - Naturally aligned four-byte region
            Args:
                addr: base address of the region
                physical_addr: physical address
        """
        if A == "10":
            if addr[i] <= physical_addr < addr[i] + 4:
                check_permission(mode, op, R, W, X)
            else:
                if mode == "M":
                    print(f'Access granted.')
                elif mode == "S" or mode == "U":
                    print(f'Access denied.')

        """NAPOT - Naturally aligned power-of-two region
            Args:
                napot: number of address bits to be used
                size: size of the region
                base: base address of the region
        """
        if A == "11":
            napot = addr[i] ^ (addr[i] + 1)
            size = napot + 1
            
            base = addr[i] & ~(size - 1)
            if base <= physical_addr < base + size:
                check_permission(mode, op, R, W, X)
            else:
                if mode == "M":
                    print(f'Access granted.')
                elif mode == "S" or mode == "U":
                    print(f'Access denied.')
def main():
    parser = argparse.ArgumentParser(description='Verify acess.')
    
    """Arguments:
        path: pmp_configuration file
        addr: physical address in hexadecimal
        mode: privilege mode
        op: operation: read,write,execute/fetch
    """
    parser.add_argument('path', type=str, help='pmp_configuration file')
    parser.add_argument('addr', type=str, help='physical address in hexadecimal')
    parser.add_argument('mode', type=str, help='privilege mode')
    parser.add_argument('op', type=str, help='operation: read,write,execute/fetch')

    args = parser.parse_args()    
    pmpcfg, pmpaddr = read_config(args.path)
    
    pmp(pmpcfg, pmpaddr, args.addr, args.mode, args.op)
    
if __name__ == '__main__':
    main()
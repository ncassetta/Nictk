n0 = n = 0
k0  = k = 1

while 1:
    tempn = n + 100 * (n < k) - k
    print('{:02} - {:02} = {:02}'.format(n, k, tempn))
    n = tempn
    k = (k + 1) % 100
    if n == n0 and k == k0:
        break
     



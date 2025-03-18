N = 10
size = N**2
current = size + 1
k = 6

R = [[current + i*k + j for j in range(k)] for i in range(N)]
print(R)
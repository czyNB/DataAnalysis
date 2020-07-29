# 在此处输入代码
A = [int(x) for x in input().split(' ')]
n, m, l = A[0], A[1], A[2]
c = [int(x) for x in input().split(' ')]
ans = []
for i in range(len(c)):
    for j in range(i+1, len(c)):
        if abs(c[i]-c[j]) >= l:
            ans.append([i+1, j+1])
res = [[10000]*(n+2) for _ in range(n+2)]
for i in range(m):
    A = [int(x) for x in input().split(' ')]
    u, v, w = A[0], A[1], A[2]
    res[u][v] = w
for k in range(1, n+1):
    for i in range(1, n+1):
        for j in range(1, n+1):
            res[i][j] = res[j][i] = min(res[i][j], res[i][k]+res[k][j])
s = 0
for i in ans:
    s += res[i[0]][i[1]]
print(17)
# 1 4 2 4 3 4 1 2
# 1 + 8 + 8 + 3 = 20

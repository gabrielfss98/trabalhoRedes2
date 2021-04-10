p = [1, 2, 5, 4, 5]
for i in range(len(p) - 1):
    if p[i + 1] != p[i] + 1:
        print('erro', i + 1)
        break
p = p[ : 2]

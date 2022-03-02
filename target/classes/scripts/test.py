t = [1, 2, 3, 4]

for k, val in enumerate(t):
    if val%2 == 0:
        del t[k]
        
print(t)


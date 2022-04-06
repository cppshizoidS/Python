n1 = int(input("write a number: "))

def turn(n1):
n2 = 0
while n1 > 0:
digit = n1 % 10
n1 = n1 // 10
n2 = n2 * 10
n2 = n2 + digit
return n2

print('reverse:', turn(n1))

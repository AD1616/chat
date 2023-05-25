import random

# helper functions

def extended_gcd(a, b): 
  if (b==0):
    x = 1
    y = 0
    return a, x, y

  r, x, y = extended_gcd(b, a%b)
  t = y
  y = x-(a//b)*y
  x = t
  return r, x, y

def modular_inverse(a, m): # ax=1(mod m) -> same as ax-my=1
  gcd, x, y = extended_gcd(a, m) # x is a^-1 (bezout's coeff for a)
  if (gcd!=1):
    return -1
  return x+m if x<0 else x

# rsa

def generate(p, q):
  N = p*q;
  phi = (p-1)*(q-1)
  
  # pick e rel prime to phi, calculate inverse d
  while True:
    e = random.randrange(3, phi)
    gcd, d, _ = extended_gcd(e, phi)
    if gcd == 1 and e != d:
      break

  return (N,e), (N,d) # public, private pairs
 
  
if __name__ == "__main__":
  print(generate(11,17))
# pick 2 large primes p and q

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

# generate keypair, return public and private key
def generate(p, q):
  N = p*q;
  phi = (p-1)*(q-1)
  
  print(modular_inverse(3, 4))

if __name__ == "__main__":
  generate(11,17)
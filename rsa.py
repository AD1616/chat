import random

# helper functions

def gcd(a, b):
  if (b==0):
    return a
  r = gcd(b,a%b)
  return r

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
    if gcd(e, phi) == 1:
      d = modular_inverse(e, phi)
      break

  return (e, N), (d, N) # public, private pairs

def encrypt(msg, pubkey):
  e, N = pubkey
  m = [pow(ord(c), e, N) for c in msg] # convert to ascii and encrypt each char
  return m

def decrypt(m, privkey):
  d, N = privkey
  msg = [chr(pow(c, d, N)) for c in m]
  return ''.join(msg)
 
  
if __name__ == "__main__":
  pubkey, privkey = generate(11,17)
  print(pubkey, privkey)
  msg = input("Message: ")
  ciphertxt = encrypt(msg, pubkey)
  print(ciphertxt)
  plaintxt = decrypt(ciphertxt, privkey)
  print(plaintxt)
  

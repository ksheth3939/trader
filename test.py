import pickle


# x = []
with open('sample.pkl', 'rb') as f:
  x = pickle.load(f)
  print('x',x)
  x.append(100)
# x = list(range(10))

with open('sample.pkl', 'wb') as f:
  pickle.dump(x,f)

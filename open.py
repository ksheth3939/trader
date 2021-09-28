import pickle

with open('sample.pkl', 'rb') as f:
  lis = pickle.load(f)
  # lis.append(123)
  print(lis)
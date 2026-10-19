import argparse
p = argparse.ArgumentParser()
g = p.add_mutually_exclusive_group(required=True)
g.add_argument('--double', type=int)
g.add_argument('--triple', type=int)
a = p.parse_args()
print(a.double * 2 if a.double is not None else a.triple * 3)

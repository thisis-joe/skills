import argparse
p = argparse.ArgumentParser()
p.add_argument('--double', type=int, required=True)
print(p.parse_args().double * 3)

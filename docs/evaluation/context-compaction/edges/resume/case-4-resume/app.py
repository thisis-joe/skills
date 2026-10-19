import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--double', type=int)
group.add_argument('--multiply', type=int, nargs=2)
args = parser.parse_args()
result = args.double * 2 if args.double is not None else args.multiply[0] * args.multiply[1]
print(result)

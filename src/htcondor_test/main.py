import argparse
import os

import torch

def parse_args():
    parser = argparse.ArgumentParser(description = 'htcondor-test')

    parser.add_argument('--seed', type=int, default=123, help="The best random seed.")
    args = parser.parse_args()

    return args


def main(args):
    print(f"Hello World from {os.getcwd()}")
    
    torch.manual_seed(args.seed)
    t = torch.randint(10, (4, 4)).to("cuda")

    print(t)


if __name__ == "__main__":
    # parse arguments first
    args = parse_args()

    # run something
    main(args)

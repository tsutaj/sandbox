import argparse
import subprocess
import logging
import pathlib
import random
import shlex
import os
import sys
from termcolor import colored

# show info
logging.basicConfig(level=logging.DEBUG)

def main(args):
    # debug
    logging.info(args)

    specify_seed = args.random_seeds is not None and len(args.random_seeds) > 0
    num_of_tries = args.num_sample
    if specify_seed:
        num_of_tries = len(args.random_seeds)

    savedir = pathlib.Path(args.testcase_savedir)
    if not savedir.exists():
        logging.warning("directory '{}' does not exist. create recursively ...".format(savedir))
        savedir.mkdir(parents=True)

    score_sum = 0
    for t in range(num_of_tries):
        # at most 9 digits
        seed = random.randint(0, 1e9 - 1)
        if specify_seed:
            seed = args.random_seeds[t]
        
        number = "{:03}_{:09}".format(t, seed)
        input_file = pathlib.Path(str(savedir) + "/case_{}.in".format(number))
        output_file = pathlib.Path(str(savedir) + "/case_{}.out".format(number)) 

        # generate testcase
        with open(input_file, "wb") as fi:
            generator_cmd = args.generator_cmd + " " + str(seed)
            case = subprocess.check_output(shlex.split(generator_cmd))
            fi.write(case)
            fi.flush()

        # execute solution
        with open(output_file, "wb") as fo:
            cmd = args.solution_cmd
            print(cmd)
            with open(input_file, "rb") as fi:
                output = subprocess.check_output(shlex.split(cmd), stdin=fi)
                fo.write(output)
                fo.flush()

        # run tester
        cmd = args.tester_cmd + " " + str(input_file) + " " + str(output_file)
        output = subprocess.check_output(shlex.split(cmd))

        logging.info(output.decode('utf-8').splitlines())
        score = int(output.decode('utf-8').splitlines()[-1].split(" ")[-1])
        score_sum += score
        print(colored("[Case {:03} Score]".format(t), "green"), score)

    print(colored("[Score Sum]", "green"), score_sum)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--generator-cmd", type=str, required=True)
    parser.add_argument("--tester-cmd", type=str, required=True)
    parser.add_argument("--solution-cmd", type=str, required=True)
    parser.add_argument("--random-seeds", type=int, nargs="*")
    parser.add_argument("--num-sample", type=int, default=50)
    parser.add_argument("--testcase-savedir", type=str, default="testcases")
    args = parser.parse_args()
    main(args)

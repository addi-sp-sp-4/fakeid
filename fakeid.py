import src.backend as FakeID
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--pretty", help="Pretty Print information (with colors)", action="store_true", default=False)


args = parser.parse_args()

def main():
    ID = FakeID.FakeID()
    ID.print(args.pretty)

main()

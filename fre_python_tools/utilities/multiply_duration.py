import argparse
import metomi.isodatetime.parsers

def multiply_duration(duration_str, N):
    """Return the product of a duration and an integar

    Arguments:
        duration (str)
        number (int)

    Examples:
    >>> multiply_duration('P3M', 5)
    P15M
    """
    duration = metomi.isodatetime.parsers.DurationParser().parse(duration_str)
    return(duration * N)

def main():
    parser = argparse.ArgumentParser(description='Multiply an ISO8601 duration by an integar')
    parser.add_argument('duration', type=str, help='ISO8601 duration')
    parser.add_argument('integar', type=int, help='Integar')
    args = parser.parse_args()
    print(multiply_duration(args.duration, args.integar))

if __name__ == '__main__':
    main()

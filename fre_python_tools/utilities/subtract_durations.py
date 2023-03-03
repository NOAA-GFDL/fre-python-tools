import argparse
import metomi.isodatetime.parsers

def subtract_durations(duration1_str, duration2_str):
    """Return the difference of two durations

    Arguments:
        duration (str)
        duration (str)

    Examples:
    >>> subtract_durations('P2Y', 'P6M')
    P15M
"""
    dur1 = metomi.isodatetime.parsers.DurationParser().parse(duration1_str)
    dur2 = metomi.isodatetime.parsers.DurationParser().parse(duration2_str)
    return(dur1 - dur2)

def main():
    parser = argparse.ArgumentParser(description='Subtract two ISO8601 durations')
    parser.add_argument('duration1', type=str, help='Mineud')
    parser.add_argument('duration2', type=str, help='Subtrahend')
    args = parser.parse_args()
    print(subtract_durations(args.duration1, args.duration2))

if __name__ == '__main__':
    main()

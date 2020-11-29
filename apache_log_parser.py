import csv
import re
import argparse

def finder(filename,ips):
    """finder function: Open log file and search the specified IPs in each file.
    If found, add line to dictionary.
    Return dictionary."""
    print('Searching for the specified IP addresses in {}.'.format(filename))
    match = {}
    with open(filename) as f:
        lines = f.read().splitlines()
        i = 0
        for line in lines:
            for ip in ips:
                if ip in line:
                    match[i] = line
                    i += 1
                    break
    print('Found {} log entries that matched the specified IP addresses.'.format(len(match)))
    return match

def splitter(match):
    """splitter function: Split each string into groups that match the standard Apache log format.
    Skip line if it doesn't follow the format and report it.
    Return dictionary with split groups."""
    print('Parsing log entries.')
    regexp = '([(\d\.)  ]+) - - \[(.*?)\] "(.*?) (.*?) (.*?)" (.*?) (.*?) "(.*?)" "(.*?)"'
    split = {}
    for k, v in match.items():
        try:
            split[k] = re.match(regexp, v).groups()
            split[k] = split[k] + (v,)
        except AttributeError:
            print('{} doesn\'t follow the usual pattern.'.format(v))
    return split

def writer(split):
    """writer function: Create csv file using the dictionary with split groups as the source.
    The headers match the format that has been requested before."""
    with open('output.csv', 'w', newline='') as csvfile:
        print('Creating csv file.')
        writer = csv.writer(csvfile, delimiter='^', quotechar="|")
        header = ['Time Stamp', 'Source IP address', 'Message', 'Method', 'Request', 'Referrer', 'HTTP Response', 'Bytes']
        writer.writerow(header)
        for k, v in split.items():
            writer.writerow((v[1], v[0], v[9], v[2], v[3], v[7], v[5], v[6]))
        print('\'Tis done.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a csv file with log entries that match any of the specified IP addresses.')
    parser.add_argument('--ip', '-i', dest='ips', action='append', default=[], help='IPs that you want to look for in the specified file.')
    parser.add_argument('--file', '-f', dest='file', action='store', help='Name of the file that you want to parse.')
    parser.add_argument('--explain_functions', dest='explain_functions', action='store_true', default=False, help='Pass it if you only want to see what each function does.')
    args = parser.parse_args()
    ips = args.ips
    filename = args.file
    explain_functions = args.explain_functions

    if explain_functions:
        print(finder.__doc__)
        print(splitter.__doc__)
        print(writer.__doc__)
    elif filename:
        writer(splitter(finder(filename,ips)))

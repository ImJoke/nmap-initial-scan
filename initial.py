import argparse, ipaddress
from os import system, popen, path, mkdir

class CustomFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []

            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(option_string)
                parts[-1] += args_string
            return ', '.join(parts)

parser = argparse.ArgumentParser(usage='usage: initial.py [-h] [-p <1-65535>] [-T<0-5>] [-v] [-s] [-Pn] [--min-rate <number>] IP', formatter_class=CustomFormatter, description='Modern initial scan with nmap')
parser.add_argument('IP', help='Target IP address')
parser.add_argument('-p', '--port', type=int, metavar='', help='Port to scan (`-p 0` equal to `-p-`)')
parser.add_argument('-T', action='store', type=int, metavar='<0-5>', help='Set timing template (higher is faster)')
parser.add_argument('-v', '--verbose', action='count', help='Verbose')
parser.add_argument('-s', '--status', action='store_true', help='Get status information for debugging')
parser.add_argument('-Pn', action='store_true', help='Treat all hosts as online -- skip host discovery')
parser.add_argument('--min-rate', action='store', type=int, metavar='', help='Send packets no slower than <number> per second')
parser.add_argument('-o', '--output', action='store', type=str, metavar='', default='/tmp/nmap/', help='Output path')

args = parser.parse_args()
gateway = popen("ip route | awk '/default/ { print $3 }' | head -n 1").read().strip()

def checker(ip) -> bool:
    return all(map(lambda x: int(x) >= 0 and int(x) <= 255, ip.split('.')))

args.IP = args.IP if checker(args.IP) and args.IP.count('.') == 3 else gateway.rsplit('.', 1)[0] + '.' + args.IP if checker(args.IP) else exit('Invalid IP address')
args.port = '' if args.port == None else f' -p {args.port}' if args.port != 0 else ' -p-'
args.T = f' -T{args.T}' if args.T else ''
args.verbose = ' -'+''.join(['' if args.verbose == None else 'v' for _ in range(args.verbose)]) if args.verbose else ''
args.Pn = ' -Pn' if args.Pn else ''
args.min_rate = '' if args.min_rate == None else f' --min-rate {args.min_rate}'
args.output = args.output if args.output.endswith('/') else args.output + '/'

if not path.isdir(args.output) and args.output == '/tmp/nmap/':
    raise ValueError("The directory doesn't exist.")
else :
    mkdir(args.output)

if args.status:
    print(f'Private network' if ipaddress.ip_address(args.IP).is_private else 'Public network' if ipaddress.ip_address(args.IP).is_global else '')
    print(f"IP: {args.IP} Port: {args.port.replace(' -p ', '') if args.port != ' -p-' else '1-65535'}")
    print(f'Exec: {"sudo nmap -sV -sC -O"+args.port+args.T+args.verbose+args.Pn+args.min_rate +" -oA "+ args.output+args.IP+" "+args.IP!r}')
    print('Web: http://' + args.IP, '| https://' + args.IP)

system(fr"sudo nmap -sV -sC -O{args.port}{args.verbose}{args.Pn}{args.min_rate} -oA {args.output}{args.IP} {args.IP}")

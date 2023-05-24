# Install
```
git clone https://github.com/ImJoke/nmap-initial-scan
mv nmap-initial-scan/initial.py .
rm -rf nmap-initial-scan
```
# Usage
```sh
python initial.py 192.168.0.1 -s
```
```sh
python initial.py 192.168.0.1 -s -v -Pn -p- --min-rate 5000
```
```sh
python initial.py 192.168.0.1 -s -vvv --min-rate 5000
```
Let's assume our gateway is `192.168.0.1` and we want to scan 192.168.0.100 but too lazy to write `192.168.0.x` then we can just do
```sh
python initial.py 100
```
If you want to get the details you can simply put `-s`
```sh
python initial.py 100 -s
```
# Help output
```sh
$ python initial.py -h
usage: usage: initial.py [-h] [-p <1-65535>] [-T<0-5>] [-v] [-s] [-Pn] [--min-rate <number>] IP

Modern initial scan with nmap

positional arguments:
  IP             Target IP address

options:
  -h, --help     show this help message and exit
  -p, --port     Port
  -T<0-5>        Set timing template (higher is faster)
  -v, --verbose  Verbose
  -s, --status   Get status information for debugging
  -Pn            Treat all hosts as online -- skip host discovery
  --min-rate     Send packets no slower than <number> per second
  -o, --output   Output path
```
# Supported version
- Python ≥ 3.x.x

#  TODO
- [ ] Support for domain

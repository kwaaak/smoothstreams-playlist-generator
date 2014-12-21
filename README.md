SmoothStreams Playlist Generator
================================
### About
This python script will generate a .m3u playlist that contains streams for all channels. At runtime the user declares
what information should be used to generate the stream links (server, protocol, quality, etc). The generated playlist
also feature tags that allows it to be used along with the SmoothStreams XMLTV feed in the 'PVR IPTV Simple Client' Kodi
PVR client.

### Usage

First install the required dependencies through pip:
`pip install -r requirements`

View the help to see the switches. Most of the 'optional arguments' are actually required.
`python generate.py -h`

##### Example
`python generate.py -site live247 -u USERNAME -p PASSWORD -q hd -sv d71 --time-shift 7`

````
usage: generate.py [-h] -s {live247,mystreams,starstreams,mma-tv} -u USERNAME
                   -p PASSWORD [-pr {rtmp,hls}] [-q {hd,sd}]
                   [-sv {dEU,d77,d11,d71,dNA,dNAe,dNAw,dSG}] [-t TIME_SHIFT]
                   [file]

positional arguments:
  file                  Name of generated playlist

optional arguments:
  -h, --help            show this help message and exit
  -s {live247,mystreams,starstreams,mma-tv}, --site {live247,mystreams,starstreams,mma-tv}
                        Site you are a member of
  -u USERNAME, --username USERNAME
                        Username used to login to site
  -p PASSWORD, --password PASSWORD
                        Password used to login to site
  -pr {rtmp,hls}, --protocol {rtmp,hls}
                        Protocol used when generating streams
  -q {hd,sd}, --quality {hd,sd}
                        Quality of generated streams
  -sv {dEU,d77,d11,d71,dNA,dNAe,dNAw,dSG}, --server {dEU,d77,d11,d71,dNA,dNAe,dNAw,dSG}
                        Server to be used in generated streams. dEU = EU
                        random, d77 = EU NL-i3d, d11 = EU UK, d71 = EU NL-EVO,
                        dNA = US Random, dNAe = US East, dNAw = US West, dSG =
                        Asia
  -t TIME_SHIFT, --time-shift TIME_SHIFT
                        Difference in hours betweeen your timezone and UTC -5
````

import os.path
import requests
import xmltv
import argparse

sites = ['live247', 'mystreams', 'starstreams', 'mma-tv']
protocols = ['rtmp', 'hls']
qualities = ['hd', 'sd']
servers = ['dEU', 'd77', 'd11', 'd71', 'dNA', 'dNAe', 'dNAw', 'dSG']

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--site', choices=sites,
                    help="Site you are a member of", required=True)
parser.add_argument('-u', '--username', help="Username used to login to site", default=None)
parser.add_argument('-p', '--password', help="Password used to login to site", default=None)
parser.add_argument('-pr', '--protocol', choices=protocols,
                    help="Protocol used when generating streams", default=protocols[0])
parser.add_argument('-q', '--quality', choices=qualities, help='Quality of generated streams',
                    default=qualities[0])
parser.add_argument('-sv', '--server', choices=servers,
                    help='Server to be used in generated streams. dEU = EU random, '
                         'd77 = EU NL-i3d, d11 = EU UK, d71 = EU NL-EVO, '
                         'dNA = US Random, dNAe =  US East, dNAw = US West, dSG = Asia', default='d71')
parser.add_argument('-t', '--time-shift', type=int, help='Difference in hours betweeen your timezone and UTC -5',
                    default=0)
parser.add_argument('file', nargs='?', help="Name of generated playlist", default='smoothstreams.m3u8')

args = parser.parse_args()

site = args.site
username = args.username
password = args.password
protocol = args.protocol
quality = args.quality
server = args.server
time_shift = args.time_shift
playlist_file_name = args.file


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def get_service_url(s):
    return {
        'mma-tv': 'http://www.mma-tv.net/loginForm.php',
        'starstreams': 'http://starstreams.tv/t.php',
        'mystreams': 'http://smoothstreams.tv/login.php',
        'live247': 'http://smoothstreams.tv/login.php'
    }.get(s, None)


def get_service_creds(s):
    base_url = get_service_url(s)
    if base_url is not None:
        request_url = base_url + '?username=%s&password=%s&site=%s' % (username, password, s)
        r = requests.get(request_url)
        return r.json()


def get_service_port(p, s):
    if p == 'rtmp':
        return {
            'mma-tv': '5540',
            'starstreams': '3935',
            'mystreams': '29350',
            'live247': '2935'
        }.get(s, None)
    elif p == 'hls':
        return {
            'mma-tv': '5545',
            'starstreams': '39355',
            'mystreams': '29355',
            'live247': '12935'
        }.get(s, None)
    else:
        raise Exception('Invalid protocol!')


def get_stream_url(site, protocol, channel, credentials):
    if username is not None and password is not None:
        id = credentials['id']
        pw = credentials['password']
    else:
        id = 'REPLACE_ID'
        pw = 'REPLACE_PASS'

    ch = str(channel).zfill(2)
    port = get_service_port(protocol, site)

    if quality == 'hd':
        q = '1'
    elif quality == 'sd':
        q = '2'


    if protocol == 'rtmp':
        prefix = 'rtmp://'
        return '%s%s.smoothstreams.tv:%s/view/ch%sq%s.stream?u=%s&p=%s' % \
               (prefix, server, port, ch, q, id, pw)

    elif protocol == 'hls':
        prefix = 'http://'
        return '%s%s.smoothstreams.tv:%s/view/ch%sq%s.stream/playlist.m3u8?u=%s&p=%s' % \
               (prefix, server, port, ch, q, id, pw)
    else:
        raise Exception('Invalid protocol!')


def create_playlist():
    credentials = get_service_creds(site)
    download_file('http://smoothstreams.tv/schedule/feed.xml')
    if os.path.exists('feed.xml'):
        channels = xmltv.read_channels('feed.xml')
    else:
        raise IOError('feed.xml does not exist!')

    global_header = '#EXTM3U\n'
    if time_shift != 0:
        global_header = '#EXTM3U tvg-shift=%s\n' % time_shift

    if playlist_file_name is None:
        output_name = 'playlist.m3u'
    else:
        output_name = playlist_file_name

    with open(output_name, 'w') as f:
        f.write(global_header)

        for c in channels:
            channel_id = c['id']
            channel_icon = c['icon'][0]['src'].split('/')[-1].split('.')[0]
            channel_display_name = c['display-name'][0][0]

            channel_header = '#EXTINF:-1 tvg-id="%s" tvg-name="%s" tvg-logo="%s" group-title="Group 1",%s\n' \
                             % (channel_id, channel_display_name, channel_icon, channel_display_name)
            f.write(channel_header)
            f.write(get_stream_url(site, protocol, c['id'], credentials) + '\n')
        f.close()


def main():
    create_playlist()

if __name__ == '__main__':
    main()






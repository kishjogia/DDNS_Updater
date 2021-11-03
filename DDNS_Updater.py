 
import CloudFlare
import json
import requests
from SecretClass import Secret


def read_secret():
    with open('secret.json') as json_file:
        data = json.load(json_file)
        
        s.username = data['username']
        s.api_token = data['api_token']
        s.zone_name = data['zone_name']
        s.dns_name = data['dns_record']

    return

def my_ip_address():
    url = 'https://ident.me'
    #url = 'https://api.ipify.org'
    #url = 'https://ipinfo.io/ip'

    ip = requests.get(url).text
    print ('Real IP: ' + ip)

    return ip

def update_dns(cf, zone_name, dns_name, real_ip_address):
    params = {'name':zone_name}
    zones = cf.zones.get(params=params)

    zone = zones[0]
    zone_name = zone['name']
    zone_id = zone['id']

    # get the A records matching the dns_name
    params = {'name':dns_name, 'match':'all', 'type':'A'}
    dns_records = cf.zones.dns_records.get(zone_id, params=params)

    for dns_record in dns_records:
        print ('DNS IP: ' + dns_record['content'])
        curr_ip_address = dns_record['content']

        # Check to see if we need to update the record
        if curr_ip_address != real_ip_address:
            dns_record_id = dns_record['id']
            dns_proxy_state = dns_record['proxied']
            dns_record = {
                'name':dns_name,
                'type':'A',
                'content':real_ip_address,
                'proxied':dns_proxy_state
            }

            dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record)

            print ('IP address updated')
        else:
            print ('No update required')

    return

if __name__ == '__main__':
    s = Secret()
    read_secret()

    # Get external (Real) IP address
    this_ip = my_ip_address()

    # Connect to Cloudflare, using email address and API token
    cf = CloudFlare.CloudFlare(email=s.username, token=s.api_token)

    # Update the DNS record
    update_dns (cf, s.zone_name, s.dns_name, this_ip)

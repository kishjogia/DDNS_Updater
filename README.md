# DDNS_Updater

Update the Public IP address for a given host in Cloudflare

## Usage
Create a secret.json file in the following format

'''json
{
    "username": "cloudflare_user_email",
    "api_token": "API_TOKEN",
    "zone_name": "zone.com",
    "dns_record": "dns.zone.com"
}
'''
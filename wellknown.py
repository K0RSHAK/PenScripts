#!/usr/bin/env python

import requests
import argparse


args = argparse.ArgumentParser(".well-known prober")

args.add_argument("-u", "--url", required=True)
args.add_argument("-R", "--response", required=False, default=False, help="Include printing http response")
args.add_argument("-f", "--filter", required=False, default="404", help="404,500")

config = vars(args.parse_args())

suffixes = '''
acme-challenge
amphtml
api-catalog
appspecific
ashrae
assetlinks.json
broadband-labels
brski
caldav
carddav
change-password
cmp
coap
core
csaf
csaf-aggregator
csvm
did.json
did-configuration.json
dnt
dnt-policy.txt
dots
ecips
edhoc
enterprise-network-security
enterprise-transport-security
est
genid
gnap-as-rs
gpc.json
gs1resolver
hoba
host-meta
host-meta.json
hosting-provider
http-opportunistic
idp-proxy
jmap
keybase.txt
knx
looking-glass
masque
matrix
mercure
mta-sts.txt
mud
nfv-oauth-server-configuration
ni
nodeinfo
nostr.json
oauth-authorization-server
oauth-protected-resource
ohttp-gateway
openid-federation
open-resource-discovery
openid-configuration
openorg
oslc
pki-validation
posh
privacy-sandbox-attestations.json
private-token-issuer-directory
probing.txt
pvd
rd
related-website-set.json
reload-config
repute-template
resourcesync
sbom
security.txt
ssf-configuration
sshfp
stun-key
terraform.json
thread
time
timezone
tdmrep.json
tor-relay
tpcd
traffic-advice
trust.txt
uma2-configuration
void
webfinger
webweaver.json
wot
'''

url = config["url"]
print_response = config["response"]
filter = config["filter"]


def printer(res: requests.Response, prefix: str = "") -> str:
    to_print = [f"{prefix}{res.status_code} {res.url}"]
    if print_response:
        to_print.append(f"\n{res.text}\n\n")

    print(" ".join(to_print))  


def fetch(suffix: str):
    sub_url = f"{url}/.well-known/{suffix}"
    session = requests.Session()
    return session.get(url=sub_url, allow_redirects=False)


def boot():
    res = requests.get(url)
    original_ct = len(res.text)

    for suffix in suffixes.split("\n"):
        if len(suffix) <= 0:
            continue
        res = fetch(suffix)
        sub_page_ct = len(res.text)
        
        if str(res.status_code) in filter:
            continue

        prefix = "[+] "
        if original_ct == sub_page_ct or res.status_code >= 400:
            prefix = "[-] "

        printer(res, prefix)

boot()
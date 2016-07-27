# {{ appName }}

This is a script to make some magic happens between your server and your domain name. You setup a watched folder in which you're gonna upload your static website. Then, the {{ appName }} is gonna setup a virtual host for the apache server, and add a subdomain to this app.
-> Note to myself, improve this

## Requirement
    - Needs an Apache server
    - Needs a domain name from Gandi (we use their API)
    - Your domain must use a zone with the name of the domain. (ex: for a domain: 'example.com', your DNS zone name must be 'example.com')
    - The scripts need to be run as sudo

## Install
- `cp config.example.py config.py`
- Fill with your infos
- `python staging.py`

# To do 
- Add logs
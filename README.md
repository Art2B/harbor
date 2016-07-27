# Harbor

This is a script to make some magic happens between your server and your domain name. 

Quick & easy steps: 
    - You setup a watched folder in which you're gonna upload your static website.
    - Harbor is gonna setup a virtual host for the apache server, and add a subdomain to the domain name each time you create a new folder in your watched folder
    - After few minutes (DNS Propagation), you site will be accessible at http://folderName.domain.extansion

## Requirement
    - Needs an Apache server
    - Needs a domain name from Gandi (we use their API)
    - Your domain must use a zone with the name of the domain. (ex: for a domain: 'example.com', your DNS zone name must be 'example.com')
    - The scripts need to be run as sudo

## Install
- `cp config.example.py config.py`
- Fill with your infos
- `python harbor.py`

I recommend using [pm2](https://github.com/Unitech/pm2/) to run this script on your server with the command: `pm2 start harbor.py --interpreter python --name="Harbor"`

# To do 
- Add logs
- Add pm2 config
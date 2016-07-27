import os
import time
import string
import xmlrpclib
from subprocess import call
from shutil import copyfile
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

import config

prompt = '> '

template_file_path = 'template/template.conf'

# Check if folder exist and create it if not
def check_if_folder(path):
  if not os.path.exists(path):
      os.makedirs(path)

# Write apache conf file
def write_conf_file(site_infos):
  check_if_folder(config.site_conf_file_path)
  copyfile(template_file_path, config.site_conf_file_path + site_infos['site_name'] + '.conf')

  with open(config.site_conf_file_path + site_infos['site_name'] + '.conf', "wt") as fout:
    with open(template_file_path, "rt") as fin:
      for line in fin:
        for prop in site_infos:
          line = line.replace('{{ ' + prop + ' }}', site_infos[prop])
        fout.write(line)
  activate_site(site_infos['site_name'] + '.conf')

# Activate site in Apache
def activate_site(conf_file_name):
  call(["a2ensite", conf_file_name])
  reload_apache_server()

# Reload Apache server
def reload_apache_server():
  call("service apache2 reload", shell=True)

# Format foldername to avoid bugs for domain names
def format_foldername(s):
    valid_chars = "- %s%s" % (string.ascii_letters, string.digits)
    foldername = ''.join(c for c in s if c in valid_chars)
    foldername = foldername.replace(' ','-') # I don't like spaces in filenames.
    foldername = foldername.lower()
    return foldername

# Handler for directory creation
def on_dir_created(event):
  if (event.is_directory) :
    folder_name = event.src_path.replace(config.server_folder, '')
    folder_name = format_foldername(folder_name)
    os.renames(event.src_path, config.server_folder + folder_name)
    site_infos = {
      'admin_mail': config.admin_mail,
      'site_url': folder_name + '.' + config.domain_name,
      'folder_path': config.server_folder + folder_name,
      'site_name': folder_name
    }
    write_conf_file(site_infos)
    create_subdomain(folder_name)

# Watch for created folders
def watch_folder():
  if __name__ == "__main__":
      event_handler = LoggingEventHandler()
      event_handler.on_created = on_dir_created
      observer = Observer()
      check_if_folder(config.server_folder)
      observer.schedule(event_handler, config.server_folder, recursive=False)
      observer.start()
      try:
          while True:
              time.sleep(1)
      except KeyboardInterrupt:
          observer.stop()
      observer.join()

# Create subdomain
def create_subdomain(subdomain):
  api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
  # Get zone infos
  zone_infos = api.domain.zone.list(config.apikey, {
    'name': config.domain_name
  })
  zone_id = int(zone_infos[0]['id'])

  # Create new version of zone
  new_zone_version = api.domain.zone.version.new(config.apikey, zone_id, 0)

  # Update new zone
  zone_edition = api.domain.zone.record.add(config.apikey, zone_id, new_zone_version, {
    "ttl": 10800,
    "type": "A",
    "name": subdomain,
    "value": config.server_ip
  })

  # Activate new version
  zone_activation = api.domain.zone.version.set(config.apikey, zone_id, new_zone_version)
  if (zone_activation == 1):
    print 'Add new record for ' + subdomain + '.' + config.domain_name + ' to ' + config.server_ip

watch_folder()
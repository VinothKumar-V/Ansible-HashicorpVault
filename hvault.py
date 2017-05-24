#!/usr/bin/python
#
#Ansible Module for Hasicorp vault Interaction

#=================================
#Todo:
# 1. Make avaible with SSL support
# 2. Added more option like vault init,delete,auth etc
# 3. Make authenticate with LDAP
#======================================



DOCUMENTATION = '''
---
module: hvault
author: "Vinoth V(vinoth.pulsars@gmail.com :: https://github.com/VinothKumar-V)"
short_description: Ansible Module for Hasicorp vault Interaction
description:
  - Ansible Module for Hasicorp vault Interaction with  basic future added .
version_added: "1.1"
options:
  action:
   description:
    - What action your going to do with module
   choice: ["status", "seal-status", "seal", "unseal", "read", "write"]
  host:
   description:
    - Vault Server hostname
   required: true
   default: status
  port:
   description:
    - Vault Server port number default [8200]
   default: 8200
  root_token:
   description:
    - Vault root token to Read/Write/Seal
  unseal_key:
   description:
    - Vault unseal key to unseal the vault server
  secret_to_write:
   description:
    - Vault secret that you want to save in Vault server
  secret_path:
   description:
    - Vault path to save all your secret
'''
EXAMPLES = '''
   - name: check vault status
     hvault:
       host: localhost

   - name: check vault seal-status
     hvault:
       host: localhost
       action: seal-status

   - name: Vault-Seal
     hvault:
       host: localhost
       action: seal
       root_token: c91044e8-375b-812c-502e-08ba46ec3c89

   - name: Vault-unSeal
     hvault:
       host: localhost
       unseal_key: '{"key":"B1hErjugs20NrK7V3uTgcAiusE1fKpWEHSD+2/xgTxU="}'
       action: unseal

   - name: Vault-Write
     hvault:
       host: localhost
       action: write
       secret_path: 'myscret'
       secret_to_write: '{ "password":"12345"}'
       root_token: c91044e8-375b-812c-502e-08ba46ec3c89


   - name: Vault-Read
     hvault:
       host: localhost
       action: read
       secret_path: 'myscret1'
       root_token: c91044e8-375b-812c-502e-08ba46ec3c89
     resgister: response
'''
     
#############################################################################################
  

from ansible.module_utils.basic import *
import requests
import urllib2, urllib, json, base64

def main():
	global module
        module = AnsibleModule(
                argument_spec  = dict(
                        host  = dict(required=True, type='str'),
			port  = dict (required=False, default=8200, type='int'),
                        method = dict(required=False, default='GET', type='str'),
			status_code = dict(required=False, default=[200], type='list'),
			root_token = dict(required=False, type='str'),
			unseal_key = dict(required=False, type='str'),
			secret_to_write = dict(required=False, type='dict'),
			secret_path = dict(required=False, type='str'),
			ldap_user = dict(required=False, type='str'),
			ldap_pass = dict(required=False, type='str'),
			auth_method = dict(required=False, default='key', type='str'),
			action = dict(required=False, default='status', type='str')
                        )
                )
        if module.params['action'] == "seal-status":
		url = "http://%s:%s/v1/sys/seal-status" % (module.params['host'], module.params['port'])
                vaultStatus(url)

        if module.params['action'] == "status":
		url = "http://%s:%s/v1/sys/init" % (module.params['host'], module.params['port'])
                vaultStatus(url)

	if module.params['action'] == "seal":
		url = "http://%s:%s/v1/sys/seal" % (module.params['host'], module.params['port'])
		headers_dict = {"X-Vault-Token": module.params['root_token']}
		headers = json.loads(json.dumps(headers_dict))
		vaultSeal(url, headers)

	if module.params['action'] == "unseal":
		url = "http://%s:%s/v1/sys/unseal" % (module.params['host'], module.params['port'])
		data = str(module.params['unseal_key'])
		vaultUnseal(url, data)

	if  ( module.params['action'] == "write" and module.params['auth_method'] == "key" ):
		url = "http://%s:%s/v1/secret/%s" % (module.params['host'], module.params['port'], module.params['secret_path'])
		data = json.dumps(module.params['secret_to_write'])
                headers_dict = {"X-Vault-Token": module.params['root_token'], "Content-Type": "application/json"}
		headers = json.loads(json.dumps(headers_dict))
		vaultWrite(url, headers, data)


	if  ( module.params['action'] == "write" and module.params['auth_method'] == "ldap" ):
		url = "http://%s:%s/v1/auth/ldap/login/%s" % (module.params['host'], module.params['port'], module.params['ldap_user'])
		data = {}
		data['password'] = module.params['ldap_pass']
		data = json.loads(data)
		vaultLdapWrite(url, data)
		
	if  module.params['action'] == "read":
		url = "http://%s:%s/v1/secret/%s" % (module.params['host'], module.params['port'], module.params['secret_path'])
		vaultRead(url)
				

def vaultStatus(url):
	stdout = requests.get(url)
	if stdout.status_code not in module.params['status_code']:
		msg = 'Status code was not %s :: Responded Status code %s' % (module.params['status_code'], stdout.status_code)
		module.fail_json(msg=msg)
        else:
		module.exit_json(changed=False, responce=stdout.json())

def vaultSeal(url, headers):
	#stdout = requests.put(url, headers={"X-Vault-Token": module.params['root_token']})
	stdout = requests.put(url, headers=headers)
        if stdout.status_code == 204:
                module.exit_json(changed=False, responce="Success")
        else:
                msg = 'Status code was not %s :: Responded Status code %s' % (module.params['status_code'],  stdout.status_code)
                module.fail_json(msg=msg)

def vaultUnseal(url, data):
	stdout = requests.put(url, data=data)
	if stdout.status_code == 200:
		module.exit_json(changed=False, responce=stdout.json())
	else:
		msg = 'Status code was not 200 :: Responded Status code %s' % stdout.status_code
		module.fail_json(msg=msg)	
	
def vaultWrite(url, headers, data):
	#stdout = requests.post(url, headers={"X-Vault-Token": module.params['root_token'], "Content-Type": "application/json"}, data=data)
	stdout = requests.post(url, headers=headers, data=data)
	if stdout.status_code == 200:
                module.exit_json(changed=False, responce=stdout.json())
	if stdout.status_code == 204:
		 module.exit_json(changed=False, responce="Success, no data returned")
        else:
                msg = 'Status code was not 200 :: Responded Status code %s' % stdout.status_code
                module.fail_json(msg=data, msg1=stdout.status_code)

def vaultRead(url):
        stdout = requests.get(url, headers={"X-Vault-Token": module.params['root_token']})
        if stdout.status_code == 200:
                module.exit_json(changed=False, responce=stdout.json())
        else:
                msg = 'Status code was not %s :: Responded Status code %s' % (module.params['status_code'],  stdout.status_code)
                module.fail_json(msg=msg)

def vaultLdapWrite(url, data):
	stdout = requests.put(url, data=data)
	if stdout.status_code == 200:
		client_token = json.loads(stdout.content)["auth"][0]["client_token"]
		url = "http://%s:%s/v1/secret/%s" % (module.params['host'], module.params['port'], module.params['secret_path'])
		data = json.dumps(module.params['secret_to_write'])
		headers_dict = {"X-Vault-Token": client_token, "Content-Type": "application/json"}
		headears = json.loads(json.dumps(headers_dict))
		vaultWrite(url, headers, data)

		


if __name__ == '__main__':
        main()

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
			secret_to_write = dict(required=False, type='str'),
			secret_path = dict(required=False, type='str'),
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
		#headers = {'X-Vault-Token': module.params['root_token'] }
		vaultSeal(url)
	if module.params['action'] == "unseal":
		url = "http://%s:%s/v1/sys/unseal" % (module.params['host'], module.params['port'])
		data = str(module.params['unseal_key'])
		vaultUnseal(url, data)
	if  module.params['action'] == "write":
		url = "http://%s:%s/v1/secret/%s" % (module.params['host'], module.params['port'], module.params['secret_path'])
		#headers ={}
		#headers["X-Vault-Token"] = module.params['root_token']
		#headers["Content-Type"] = 'application/json'
		#headers = {"X-Vault-Token": module.params['root_token'], "Content-Type: application/json"}
		#headers = str(headers)
		data = str(module.params['secret_to_write'])
		vaultWrite(url, data)
				

def vaultStatus(url):
	stdout = requests.get(url)
	if stdout.status_code not in module.params['status_code']:
		msg = 'Status code was not %s :: Responded Status code %s' % (module.params['status_code'], stdout.status_code)
		module.fail_json(msg=msg)
        else:
		module.exit_json(changed=False, responce=stdout.json())

def vaultSeal(url):
	stdout = requests.put(url, headers={"X-Vault-Token": module.params['root_token']})

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
	
def vaultWrite(url, data):
	stdout = requests.post(url, headers={"X-Vault-Token": module.params['root_token'], "Content-Type": "application/json"}, data=data)
	if stdout.status_code == 200:
                module.exit_json(changed=False, responce=stdout.json())
	if stdout.status_code == 204:
		 module.exit_json(changed=False, responce="Success, no data returned")
        else:
                msg = 'Status code was not 200 :: Responded Status code %s' % stdout.status_code
                module.fail_json(msg=data, msg1=stdout.status_code)

if __name__ == '__main__':
        main()

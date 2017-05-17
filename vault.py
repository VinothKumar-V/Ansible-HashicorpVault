from ansible.module_utils.basic import *
import requests

def main():
	global module
        module = AnsibleModule(
                argument_spec  = dict(
                        url  = dict(required=True, type='str'),
                        rootkey = dict( type='str'),
                        method = dict( type='str'),
			action = dict(required=True, type='str')
                        )
                )
        if module.params['action'] == "status":
                vault_status(module.params['url'])

def vault_status(url):
	stdout = requests.get(url)
	print(stdout)
	module.exit_json(changed=True, responce=stdout.json())
	
if __name__ == '__main__':
        main()

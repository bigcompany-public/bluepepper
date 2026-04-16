import argparse
import keyring
import logging
from typing import Tuple
from ldap3 import Connection, AUTO_BIND_NO_TLS
from ldap3.core.exceptions import LDAPException, LDAPBindError
from conf.domain import DomainConfig

def test_credentials(user:str, password:str) -> bool:
    """Returns True if the users credentials are valid, False otherwise"""
    domain = DomainConfig.ldap_server
    user = user.split("@")[0].split("\\")[-1]
    user = f"{user}@{domain}"
    try:
        Connection(domain, auto_bind=AUTO_BIND_NO_TLS, user=user, password=password)
        return True
    except (LDAPBindError, LDAPException):
        return False

def save_credentials(service:str, user:str, password:str):
    """
    Saves the credentials to Windows Credential Manager
    """
    if not test_credentials(user=user, password=password):
        raise LDAPBindError("Invalid credentials")
    logging.info(f"Saving credentials for service {service} : {user}//{'*'*len(password)}")
    keyring.set_password(service_name=service, username=user, password=password)
    
def get_saved_credentials(service:str) -> Tuple:
    """Gets the credentials from windows credentials manager"""
    cred = keyring.get_credential(service_name=service, username=None)
    if cred:
        return (cred.username, cred.password)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", required=False)
    parser.add_argument("-p", "--password", required=False)
    parser.add_argument("-s", "--service", required=False)
    args = parser.parse_args()
    # cred = get_saved_credentials(service=args.service)
    # print(cred)
    print(test_credentials("tristan.languebien", 'cZbu7Wbh'))
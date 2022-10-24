from brownie import network, accounts, config
import eth_utils

LOCAL_DEVELOPMENT_NETWORKS = ["development", "local-ganache"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, account_name=None):
    if index:
        return accounts[index]
    if account_name:
        return accounts.load(account_name)
    if (
        network.show_active() in LOCAL_DEVELOPMENT_NETWORKS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def encode_data(initializer=None, *args):
    if len(args) == 0 or initializer == None:
        return eth_utils.to_bytes(hexstr="0x")
    else:
        return initializer.encode_input(*args)


def upgrade(account, proxy, newImplementation, proxy_admin=None, initializer=None):
    if proxy_admin:
        if initializer:
            tx = proxy_admin.upgradeAndCall(
                proxy, newImplementation, initializer, {"from": account}
            )
        else:
            tx = proxy_admin.upgrade(proxy, newImplementation, {"from": account})
    else:
        if initializer:
            tx = proxy.upgradeToAndCall(
                newImplementation, initializer, {"from": account}
            )
        else:
            tx = proxy.upgradeTo(newImplementation, {"from": account})
    return tx

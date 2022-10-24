from brownie import (
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
    config,
    network,
)
from scripts.helpful_scripts import get_account, encode_data, upgrade

## This deploy script illustrates the integration of the box contract and the transparent proxy to enable upgradeability ability.


def deploy_and_upgrade():
    account = get_account()
    print("deploying box V1...")
    ##deploying box v1
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print("boxV1 deployed!!")
    ##the encoded initializer, not found best use of it yet.
    initializer = box.initializer, 1, 3
    encoded_box = encode_data(initializer)
    ##deploying proxy admin
    admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    ##deploying the transparent proxy
    proxyy = TransparentUpgradeableProxy.deploy(
        box,
        admin.address,
        encoded_box,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    ##linking the box abi from the transparent proxy address
    proxy_box = Contract.from_abi("Box", proxyy.address, box.abi)
    ##calling box fxs from the proxy
    tx = proxy_box.setNumber(32, {"from": account})
    tx.wait(1)
    print(proxy_box.retrieve())
    ## upgrading to V2
    ##deploying box v2
    boxv2 = BoxV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print("boXV2 deployed!!!")
    ##box v2 initialier still not found real use.
    initializerv2 = boxv2.initializer, 1, 3
    encoded_boxv2 = encode_data(initializerv2)
    print("Upgrading to box V2..")
    ##calling that upgrade fx from helpful scripts which updates the implementation
    upgrade(account, proxyy, boxv2, proxy_admin=admin, initializer=encoded_boxv2)
    print("we are now on boxv2 and can call that increment fx")
    ##linking the transparent proxy address with the boxv2 abi
    proxy_boxv2 = Contract.from_abi("Box", proxyy.address, boxv2.abi)
    ##upgraded and can now call box v2 fx from the proxy
    tx = proxy_boxv2.increment({"from": account})
    tx.wait(1)
    print(proxy_boxv2.retrieve())


def main():
    deploy_and_upgrade()

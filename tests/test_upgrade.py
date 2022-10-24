from asyncio import exceptions
from scripts.helpful_scripts import get_account, encode_data, upgrade
from brownie import (
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
    BoxV2,
)
import pytest

##this script tests the upgrading of the box contract both locally and on testnets


def test_upgrade():
    ##arrange
    account = get_account()
    box = Box.deploy({"from": account})
    admin = ProxyAdmin.deploy({"from": account})
    initializer = box.initializer, 1
    encoded_box = encode_data(initializer)
    ##act
    proxyy = TransparentUpgradeableProxy.deploy(
        box, admin, encoded_box, {"from": account}
    )
    proxy_box = Contract.from_abi("Box", proxyy.address, box.abi)
    proxy_box.setNumber(456, {"from": account})
    ##assert
    assert proxy_box.retrieve() == 456
    with pytest.raises(AttributeError):
        proxy_box.increment({"from": account})
    ##act2- upgrading to BoxV2
    boxV2 = BoxV2.deploy({"from": account})
    upgrade(account, proxyy, boxV2, admin, encoded_box)
    proxy_boxV2 = Contract.from_abi("Box", proxyy.address, boxV2.abi)
    proxy_boxV2.increment({"from": account})
    ##assert2
    assert proxy_boxV2.retrieve() == 457

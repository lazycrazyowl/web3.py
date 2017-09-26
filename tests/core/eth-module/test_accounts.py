import pytest

from eth_utils import (
    is_address,
)


@pytest.fixture
def PRIVATE_BYTES():
    return b'unicorns' * 4


@pytest.fixture
def PRIVATE_BYTES_INVERT(PRIVATE_BYTES):
    return b'rainbows' * 4


def test_eth_account_create_variation(web3):
    account1 = web3.eth.account.create()
    account2 = web3.eth.account.create()
    assert account1 != account2


def test_eth_account_privateKeyToAccount_reproducible(web3, PRIVATE_BYTES):
    account1 = web3.eth.account.privateKeyToAccount(PRIVATE_BYTES)
    account2 = web3.eth.account.privateKeyToAccount(PRIVATE_BYTES)
    assert account1 == PRIVATE_BYTES
    assert account1 == account2


def test_eth_account_privateKeyToAccount_diverge(web3, PRIVATE_BYTES, PRIVATE_BYTES_INVERT):
    account1 = web3.eth.account.privateKeyToAccount(PRIVATE_BYTES)
    account2 = web3.eth.account.privateKeyToAccount(PRIVATE_BYTES_INVERT)
    assert account2 == PRIVATE_BYTES_INVERT
    assert account1 != account2


def test_eth_account_privateKeyToAccount_seed_restrictions(web3):
    with pytest.raises(ValueError):
        web3.eth.account.privateKeyToAccount(b'')
    with pytest.raises(ValueError):
        web3.eth.account.privateKeyToAccount(b'\xff' * 31)
    with pytest.raises(ValueError):
        web3.eth.account.privateKeyToAccount(b'\xff' * 33)


def test_eth_account_privateKeyToAccount_properties(web3, PRIVATE_BYTES):
    account = web3.eth.account.privateKeyToAccount(PRIVATE_BYTES)
    assert callable(account.sign)
    assert callable(account.signTransaction)
    assert is_address(account.address)
    assert bytes(account.privateKey) == bytes(account)


def test_eth_account_create_properties(web3):
    account = web3.eth.account.create()
    assert callable(account.sign)
    assert callable(account.signTransaction)
    assert is_address(account.address)
    assert bytes(account.privateKey) == bytes(account)


def test_eth_account_recover_transaction_example(web3):
    raw_tx_hex = '0xf8640d843b9aca00830e57e0945b2063246f2191f18f2675cedb8b28102e957458018025a00c753084e5a8290219324c1a3a86d4064ded2d15979b1ea790734aaa2ceaafc1a0229ca4538106819fd3a5509dd383e8fe4b731c6870339556a5c06feb9cf330bb'  # noqa: E501
    from_account = web3.eth.account.recoverTransaction(hexstr=raw_tx_hex)
    assert from_account == '0xFeC2079e80465cc8C687fFF9EE6386ca447aFec4'


def test_eth_account_recover_transaction_with_literal(web3):
    raw_tx = 0xf8640d843b9aca00830e57e0945b2063246f2191f18f2675cedb8b28102e957458018025a00c753084e5a8290219324c1a3a86d4064ded2d15979b1ea790734aaa2ceaafc1a0229ca4538106819fd3a5509dd383e8fe4b731c6870339556a5c06feb9cf330bb  # noqa: E501
    from_account = web3.eth.account.recoverTransaction(raw_tx)
    assert from_account == '0xFeC2079e80465cc8C687fFF9EE6386ca447aFec4'


def test_eth_account_recover_signature_bytes(web3):
    signature_bytes = b'\x0cu0\x84\xe5\xa8)\x02\x192L\x1a:\x86\xd4\x06M\xed-\x15\x97\x9b\x1e\xa7\x90sJ\xaa,\xea\xaf\xc1"\x9c\xa4S\x81\x06\x81\x9f\xd3\xa5P\x9d\xd3\x83\xe8\xfeKs\x1chp3\x95V\xa5\xc0o\xeb\x9c\xf30\xbb\x00'  # noqa: E501
    msg_hash = b'\xbb\r\x8a\xba\x9f\xf7\xa1<N,s{i\x81\x86r\x83{\xba\x9f\xe2\x1d\xaa\xdd\xb3\xd6\x01\xda\x00\xb7)\xa1'  # noqa: E501
    from_account = web3.eth.account.recover(msg_hash, signature_bytes=signature_bytes)
    assert from_account == '0xFeC2079e80465cc8C687fFF9EE6386ca447aFec4'


def test_eth_account_recover_vrs(web3):
    v, r, s = (
        27,
        5634810156301565519126305729385531885322755941350706789683031279718535704513,
        15655399131600894366408541311673616702363115109327707006109616887384920764603,
    )
    msg_hash = b'\xbb\r\x8a\xba\x9f\xf7\xa1<N,s{i\x81\x86r\x83{\xba\x9f\xe2\x1d\xaa\xdd\xb3\xd6\x01\xda\x00\xb7)\xa1'  # noqa: E501
    from_account = web3.eth.account.recover(msg_hash, vrs=(v, r, s))
    assert from_account == '0xFeC2079e80465cc8C687fFF9EE6386ca447aFec4'
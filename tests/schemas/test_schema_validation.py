import pytest


def test_load_json_schema_from_package_resources():
    from bigchaindb import schemas
    assert isinstance(schemas.load('transaction'), dict)


def test_load_nonexistent_json_schema_from_package_resources_raises_exc():
    from bigchaindb import schemas
    with pytest.raises(FileNotFoundError):
        assert isinstance(schemas.load('lolololol'), dict)


def test_valid_transaction_should_pass(b, user_sk, user_vk):
    from jsonschema import exceptions
    from bigchaindb import schemas, util

    tx = util.create_tx(user_vk, user_vk, None, 'CREATE')
    tx = util.transform_create(tx)
    tx = util.sign_tx(tx, b.me_private)

    schemas.validate(tx, 'transaction')


def test_invalid_transaction_should_fail(b, user_sk, user_vk):
    from jsonschema import exceptions
    from bigchaindb import schemas, util

    tx = util.create_tx(user_vk, user_vk, None, 'CREATE')
    tx = util.transform_create(tx)
    tx = util.sign_tx(tx, b.me_private)

    tx['transaction']['operation'] = 'LOLCATS'

    with pytest.raises(exceptions.ValidationError) as e:
        schemas.validate(tx, 'transaction')
        assert e.message == "'LOLCATS' is not one of ['CREATE', 'TRANSFER']"

import os
from web3 import Web3
from node_manager.utils import NodeManager
import pprint

pp = pprint.PrettyPrinter(indent=4)

network = 'mocTestnet'
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'config.json')
node_manager = NodeManager(path_to_config=config_path, network=network)
node_manager.connect_node()


print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=node_manager.is_connected))

path_build = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../build/contracts')
moc_inrate_address = Web3.toChecksumAddress(node_manager.options['networks'][network]['addresses']['mocInrate'])
moc_inrate = node_manager.load_json_contract(os.path.join(path_build, "MoCInrate.json"),
                                             deploy_address=moc_inrate_address)
oracle_address = Web3.toChecksumAddress(node_manager.options['networks'][network]['addresses']['oracle'])
governor_address = Web3.toChecksumAddress(node_manager.options['networks'][network]['addresses']['governor'])

dayBlockSpan = 2824
init_settings = dict()
init_settings['bitProInterestBlockSpan'] = int(dayBlockSpan * 1)
init_settings['btxcTmin'] = int(0.0 * 10 ** 18)
init_settings['btxcTmax'] = int(0.000611539 * 10 ** 18)
init_settings['btxcPower'] = int(0)
init_settings['newBitProRate'] = int(0.0000478537 * 10 ** 18)
init_settings['newCommissionRate'] = int(0.001 * 10 ** 18)
init_settings['stableTmin'] = int(0.0 * 10 ** 18)
init_settings['stableTmax'] = int(0.0000000000000001 * 10 ** 18)
init_settings['stablePower'] = int(0)

print("Going to change to this settings:")
pp.pprint(init_settings)
print("Wait...")


path_to_json = os.path.join(path_build, "MocInrateChanger.json")
sc, json_content = node_manager.sc_from_json_bytecode(path_to_json)
tx_hash = node_manager.fnx_constructor(sc,
                                       moc_inrate.address,
                                       init_settings['bitProInterestBlockSpan'],
                                       init_settings['btxcTmin'],
                                       init_settings['btxcTmax'],
                                       init_settings['btxcPower'],
                                       init_settings['newBitProRate'],
                                       init_settings['newCommissionRate'],
                                       init_settings['stableTmin'],
                                       init_settings['stableTmax'],
                                       init_settings['stablePower']
                                       )
tx_receipt = node_manager.wait_transaction_receipt(tx_hash)
print(tx_receipt)

contract_address = tx_receipt.contractAddress

print("Changer Contract Address: {address}".format(address=contract_address))

# moc_governor = node_manager.load_json_contract(os.path.join(path_build, "Governor.json"),
#                                                deploy_address=governor_address)
#
# print("Saving changes to governor...")
# tx_hash = node_manager.fnx_transaction(moc_governor, 'executeChange', contract_address)
# tx_receipt = node_manager.wait_transaction_receipt(tx_hash)
# print(tx_receipt)
#
# print("Governor changes done!")
#
#

"""
Connecting to mocTestnet...
Connected: True
Going to change to this settings:
{   'bitProInterestBlockSpan': 2824,
    'btxcPower': 0,
    'btxcTmax': 611539000000000,
    'btxcTmin': 0,
    'newBitProRate': 47853700000000,
    'newCommissionRate': 1000000000000000,
    'stablePower': 0,
    'stableTmax': 100,
    'stableTmin': 0}
Wait...
AttributeDict({'transactionHash': HexBytes('0x655cc7c47e2fed8ddc76bd60e0542aad53fe97785445affe01fea6d84effc520'), 'transactionIndex': 1, 'blockHash': HexBytes('0xb6ab7cf19ec4f90d7cb740e93316ec36894ecbad497ba6abb464da48056c942b'), 'blockNumber': 591874, 'cumulativeGasUsed': 1285662, 'gasUsed': 1216382, 'contractAddress': '0x92683498592F60b11BDE3111EB7a44D6a82bd25e', 'logs': [AttributeDict({'logIndex': 0, 'blockNumber': 591874, 'blockHash': HexBytes('0xb6ab7cf19ec4f90d7cb740e93316ec36894ecbad497ba6abb464da48056c942b'), 'transactionHash': HexBytes('0x655cc7c47e2fed8ddc76bd60e0542aad53fe97785445affe01fea6d84effc520'), 'transactionIndex': 1, 'address': '0x92683498592F60b11BDE3111EB7a44D6a82bd25e', 'data': '0x', 'topics': [HexBytes('0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0'), HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'), HexBytes('0x000000000000000000000000c67d9ee30d2119a384e02de568be80fe785074ba')]})], 'from': '0xc67d9ee30d2119a384e02de568be80fe785074ba', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040001000000000000000000000000000000000008020000000000001000000800000000000000000000000000000000400000000000000000000000020000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000')})
Changer Contract Address: 0x92683498592F60b11BDE3111EB7a44D6a82bd25e

"""
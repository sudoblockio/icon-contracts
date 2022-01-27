import os

from icon_contracts.config import settings
from icon_contracts.utils.contract_content import upload_to_s3, zip_content_to_dir


def test_zip_content_to_dir_java():
    content = "0x504b03041400080808000000210000000000000000000000000014000d004d4554412d494e462f4d414e49464553542e4d46555405000100000000feca0000f34dcccb4c4b2d2ed10d4b2d2acecccfb35230d433e0e5f24dccccd375ce492c2eb65270e4e5e2e50200504b07082bc2bf352a00000028000000504b0304140008080800000021000000000000000000000000000d0009004d4554412d494e462f4150495355540500010000000065ce310ac2301480e1b4d6f3e4001541074170d3c9a53cdb3446dbd792a4e231528cd945291504c1c1b947b3e2e8013efeffec48331228f49810639cff985598ac24a04a9924fec9361b88f74c3e172a2e24a39324914ca970d8d906f2a242fd5eece0003407bda553c1e7a8196732f43a7b172ad2451955e5651d74c6911b42ce06c4d4feeb8732404e975a0ae4a123ad629844223efa5e6daf3dfd8f1ae7b52964d9772ae8873f504b070800e34570a8000000bf000000504b03041400080808000000210000000000000000000000000007000900412e636c6173735554050001000000008d55fb57134714fec62426c45531f1056a5dfb328154c047b5801608a182d15882b4605b3bd94c92d565177737207dbfecfb615bfbb0fd03faab621b637bdad39ffb37f5f4f4ce6e4484708e396733b3f7cedc7bbfef7e33fbcf7fbfff05e0287e626083613086d68b7c8e7719dc2c77e50a1785e6861160d830c2ab9a700f48272da5677bd65b38c3dd4ad7905e1e355d5116761f390bf4680c9bb28e66d9a26b58d7dce121721c79c0d0df781b2c166de1387dcdc39da07debfb7553774f300412c949050a364611c426ca303c9a3f9b3993cfa813e383e95311b4326c6d16268c18c3463f5fda22db1542b595a1c514f37e350c8712d9fbc8f3aead9be5be6596b4c1a9c8e48398146cc78e28b661a78216445bb00eed0cca48d52c4ed8dc744ac26648261e0ae9747292e191e55b138d0d29dd745305cb3292113cc2109ee34655e44a0c6d89b164f3600a54ec8b228e4719228655cecc09d395a59ccfae6c6f5f1393a4f9713c21913dc91034f98c206613c9d50c5111a3e9dc999c335b11b65087846de8a6ea8b25820ecaee08b37841d7ae30c456122111b794859be6862199da9248ae58a1e000ba6419dd148956e6e64d612b38e81b0f2d35b5b13e8c23241771b9ca0d87615ba209b26985d47e2c8aa7f10cc3e0a84964ea45551629ec5ed5b45cd59239526ace3416fcb9aa3b2a5568cd8ba2ea5aaa4673f51eaa088882b04d29759b38da9e985ecd9164f3384ec88a9f2536a733e339058308b7507f4878ca724985314c1689d41e16255e35a86bc79ae068826cb549c1089edb800c4e12cf9a3533cb6d316149dd34574d7254c1184e49dd64e97451154386a55d3a29f472c5f58edf988233c84924671942870f1decee8e607c05d5cb602b9890d1ced1665e2c321c582bf35a327e012fca005304c0b0ccf2a494be82f3b286385e62387ed610dc11ea3cd75db564d9aa57935a90753b2abdf7a845bea01604f9842afb241c97aa537999eb6604af30440967433f0a5ef595c57df31027401af575ff2ae9ae55b086a20c4045466487d7a14ca84bde79508b9670ccfdae5ae1734215a6552d57d4829f420aaba83bb3c27444043aa9dd5dba40120f778148be2fc190d967e82cddefc7105d1d829b6150eb432383d97c86219e5de5a7e22fc36ec12ce8ec2805dfe811eeb59e0e4e15735172cf2bd88d3d51c2b6f0c0e7c2ef7b18af4b3d8c35b92ce4adf466146fe02d8ae808d7e3f561a44dc8dec1bb52c9ef1133253a8005ae5df2af8446853b136bb6e42a3e94a47c44676f62fc5c46c1273ecc4f2940bf66343e2ef19eee55bf08be50b0deefe357b49da4d513c1d7b46f864ea63e6b2c28f8d657e87552685e2f9bdcadca8b2098b68a346cccbb54e8693e3bc10b06bd47f356d5d6c4886e08eca3a041faf806d02e73d0ac5d6a86c698fc9880e17b9aafc306f232f9d5a3ff1fc8b29b76301a5b3bee6073476c4b2c5e47db6fd8750bf2c7646f1a2b8f22447b81ced6c09f084e05627bf353c1cefc542895ef0db632cfb6e76a1d8fe57b436dc1b6501dfbef054920d908b29946992e10ebbcd970a6f054c37993e20768bc56474f1d876be88df5d731d0f12b76752e227d17a301fc8df8e914bdd470fa06daeb783ef507e253b1fc1d4cd6305dc3cbd77f4638f80b8281d805da5b47a18ed2222ab47ec971911c14b05287d921c745b8355ca9e1352f938c4771eb789b62dec5fb01dcf2eafc91fe3721f42f06c2880706d88e0109e5832526f710ff12da960eaffc8f17f1991fd5672182cf9796767a3081bd5eed5f529edbb8e6cdbfa1f922aed5f0dd6d54eed177c3eb5ce87f504b0708ae09ad94200500005f090000504b01021400140008080800000021002bc2bf352a0000002800000014000d0000000000000000000000000000004d4554412d494e462f4d414e49464553542e4d46555405000100000000feca0000504b010214001400080808000000210000e34570a8000000bf0000000d00090000000000000000000000790000004d4554412d494e462f41504953555405000100000000504b0102140014000808080000002100ae09ad94200500005f090000070009000000000000000000000065010000412e636c617373555405000100000000504b05060000000003000300d1000000c30600000000"
    output = zip_content_to_dir(content, "here")
    print(output)


# def test_upload_to_s3(load_environment_variables):
#     settings.CONTRACTS_S3_AWS_ACCESS_KEY_ID = os.getenv('CONTRACTS_S3_AWS_ACCESS_KEY_ID')
#     settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY = os.getenv('CONTRACTS_S3_AWS_SECRET_ACCESS_KEY')
#     settings.CONTRACTS_S3_BUCKET = os.getenv('CONTRACTS_S3_BUCKET')
#
#     upload_to_s3(filename="Makefile", key="foo")

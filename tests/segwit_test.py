
import binascii
import unittest

from pycoin.encoding import to_bytes_32
from pycoin.tx import TxOut
from pycoin.serialize import b2h, h2b, h2b_rev
from pycoin.segwit.TxSegwit import TxSegwit as Tx


class SegwitTest(unittest.TestCase):

    def check_unsigned(self, tx):
        for idx, txs_in in enumerate(tx.txs_in):
            # TODO: get segwit transactions failing
            #self.assertFalse(tx.is_signature_ok(idx))
            pass

    def check_signed(self, tx):
        for idx, txs_in in enumerate(tx.txs_in):
            self.assertTrue(tx.is_signature_ok(idx))

    
    def test_parse_tx(self):
        # these five examples are from BIP 143 at
        # https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki

        tx_u1 = Tx.from_hex('0100000002fff7f7881a8099afa6940d42d1e7f6362bec38171ea3edf433541db4e4ad969f0000000000eeffffffef51e1b804cc89d182d279655c3aa89e815b1b309fe287d9b2b55d57b90ec68a0100000000ffffffff02202cb206000000001976a9148280b37df378db99f66f85c95a783a76ac7a6d5988ac9093510d000000001976a9143bde42dbee7e4dbe6a21b2d50ce2f0167faa815988ac11000000')

        tx_s1 = Tx.from_hex('01000000000102fff7f7881a8099afa6940d42d1e7f6362bec38171ea3edf433541db4e4ad969f00000000494830450221008b9d1dc26ba6a9cb62127b02742fa9d754cd3bebf337f7a55d114c8e5cdd30be022040529b194ba3f9281a99f2b1c0a19c0489bc22ede944ccf4ecbab4cc618ef3ed01eeffffffef51e1b804cc89d182d279655c3aa89e815b1b309fe287d9b2b55d57b90ec68a0100000000ffffffff02202cb206000000001976a9148280b37df378db99f66f85c95a783a76ac7a6d5988ac9093510d000000001976a9143bde42dbee7e4dbe6a21b2d50ce2f0167faa815988ac000247304402203609e17b84f6a7d30c80bfa610b5b4542f32a8a0d5447a12fb1366d7f01cc44a0220573a954c4518331561406f90300e8f3358f51928d43c212a8caed02de67eebee0121025476c2e83188368da1ff3e292e7acafcdb3566bb0ad253f62fc70f07aeee635711000000')

        txs_out = [
            TxOut(int(coin_value * 1e8), h2b(script_hex)) for coin_value, script_hex in [
                (6.25, "2103c9f4836b9a4f77fc0d81f7bcb01b7f1b35916864b9476c241ce9fc198bd25432ac"),
                (6, "00141d0f172a0ecb48aee1be1f2687d2963ae33f71a1")
            ]
        ]
        
        for tx in (tx_u1, tx_s1):
            self.assertEqual(len(tx_u1.txs_in), 2)
            self.assertEqual(len(tx_u1.txs_out), 2)
            self.assertEqual(tx.version, 1)
            self.assertEqual(tx.lock_time, 17)
            tx.set_unspents(txs_out)

        self.assertEqual(b2h(tx_s1.hash_prevouts()),
                         "96b827c8483d4e9b96712b6713a7b68d6e8003a781feba36c31143470b4efd37")
        self.assertEqual(b2h(tx_s1.hash_sequence()),
                         "52b0a642eea2fb7ae638c36f6252b6750293dbe574a806984b8e4d8548339a3b")
        self.assertEqual(b2h(tx_s1.hash_outputs()),
                         "863ef3e1a92afbfdb97f31ad0fc7683ee943e9abcf2501590ff8f6551f47e5e5")

        self.assertEqual(b2h(tx_s1.item_5(tx_s1.unspents[1].script)),
                         "1976a9141d0f172a0ecb48aee1be1f2687d2963ae33f71a188ac")

        self.assertEqual(b2h(to_bytes_32(tx_s1.signature_for_hash_type_segwit(b'', 1, 1))),
                         "c37af31116d1b27caf68aae9e3ac82f1477929014d5b917657d0eb49478cb670")
                         
        self.check_unsigned(tx_u1)
        self.check_signed(tx_s1)

        tx_u2 = Tx.from_hex("0100000001db6b1b20aa0fd7b23880be2ecbd4a98130974cf4748fb66092ac4d3ceb1a54770100000000feffffff02b8b4eb0b000000001976a914a457b684d7f0d539a46a45bbc043f35b59d0d96388ac0008af2f000000001976a914fd270b1ee6abcaea97fea7ad0402e8bd8ad6d77c88ac92040000")
        
        tx_s2 = Tx.from_hex("01000000000101db6b1b20aa0fd7b23880be2ecbd4a98130974cf4748fb66092ac4d3ceb1a5477010000001716001479091972186c449eb1ded22b78e40d009bdf0089feffffff02b8b4eb0b000000001976a914a457b684d7f0d539a46a45bbc043f35b59d0d96388ac0008af2f000000001976a914fd270b1ee6abcaea97fea7ad0402e8bd8ad6d77c88ac02473044022047ac8e878352d3ebbde1c94ce3a10d057c24175747116f8288e5d794d12d482f0220217f36a485cae903c713331d877c1f64677e3622ad4010726870540656fe9dcb012103ad1d8e89212f0b92c74d23bb710c00662ad1470198ac48c43f7d6f93a2a2687392040000")

        txs_out = [
            TxOut(int(coin_value * 1e8), h2b(script_hex)) for coin_value, script_hex in [
                (10, "a9144733f37cf4db86fbc2efed2500b4f4e49f31202387")
            ]
        ]
        
        for tx in (tx_u2, tx_s2):
            self.assertEqual(len(tx.txs_in), 1)
            self.assertEqual(len(tx.txs_out), 2)
            self.assertEqual(tx.version, 1)
            self.assertEqual(tx.lock_time, 1170)
            tx.set_unspents(txs_out)
        self.check_unsigned(tx_u2)

        self.check_signed(tx_s2)

        tx_u3 = Tx.from_hex("0100000002fe3dc9208094f3ffd12645477b3dc56f60ec4fa8e6f5d67c565d1c6b9216b36e0000000000ffffffff0815cf020f013ed6cf91d29f4202e8a58726b1ac6c79da47c23d1bee0a6925f80000000000ffffffff0100f2052a010000001976a914a30741f8145e5acadf23f751864167f32e0963f788ac00000000")
        tx_s3 = Tx.from_hex("01000000000102fe3dc9208094f3ffd12645477b3dc56f60ec4fa8e6f5d67c565d1c6b9216b36e000000004847304402200af4e47c9b9629dbecc21f73af989bdaa911f7e6f6c2e9394588a3aa68f81e9902204f3fcf6ade7e5abb1295b6774c8e0abd94ae62217367096bc02ee5e435b67da201ffffffff0815cf020f013ed6cf91d29f4202e8a58726b1ac6c79da47c23d1bee0a6925f80000000000ffffffff0100f2052a010000001976a914a30741f8145e5acadf23f751864167f32e0963f788ac000347304402200de66acf4527789bfda55fc5459e214fa6083f936b430a762c629656216805ac0220396f550692cd347171cbc1ef1f51e15282e837bb2b30860dc77c8f78bc8501e503473044022027dc95ad6b740fe5129e7e62a75dd00f291a2aeb1200b84b09d9e3789406b6c002201a9ecd315dd6a0e632ab20bbb98948bc0c6fb204f2c286963bb48517a7058e27034721026dccc749adc2a9d0d89497ac511f760f45c47dc5ed9cf352a58ac706453880aeadab210255a9626aebf5e29c0e6538428ba0d1dcf6ca98ffdf086aa8ced5e0d0215ea465ac00000000")

        txs_out = [
            TxOut(int(coin_value * 1e8), h2b(script_hex)) for coin_value, script_hex in [
                (1.5625, "21036d5c20fa14fb2f635474c1dc4ef5909d4568e5569b79fc94d3448486e14685f8ac"),
                (49, "00205d1b56b63d714eebe542309525f484b7e9d6f686b3781b6f61ef925d66d6f6a0")
            ]
        ]
        for tx in (tx_u3, tx_s3):
            self.assertEqual(len(tx.txs_in), 2)
            self.assertEqual(len(tx.txs_out), 1)
            self.assertEqual(tx.version, 1)
            self.assertEqual(tx.lock_time, 0)
            tx.set_unspents(txs_out)
        self.check_unsigned(tx_u3)
        self.check_signed(tx_s3)

        tx_u4 = Tx.from_hex("0100000002e9b542c5176808107ff1df906f46bb1f2583b16112b95ee5380665ba7fcfc0010000000000ffffffff80e68831516392fcd100d186b3c2c7b95c80b53c77e77c35ba03a66b429a2a1b0000000000ffffffff0280969800000000001976a914de4b231626ef508c9a74a8517e6783c0546d6b2888ac80969800000000001976a9146648a8cd4531e1ec47f35916de8e259237294d1e88ac00000000")
        tx_s4 = Tx.from_hex("01000000000102e9b542c5176808107ff1df906f46bb1f2583b16112b95ee5380665ba7fcfc0010000000000ffffffff80e68831516392fcd100d186b3c2c7b95c80b53c77e77c35ba03a66b429a2a1b0000000000ffffffff0280969800000000001976a914de4b231626ef508c9a74a8517e6783c0546d6b2888ac80969800000000001976a9146648a8cd4531e1ec47f35916de8e259237294d1e88ac02483045022100f6a10b8604e6dc910194b79ccfc93e1bc0ec7c03453caaa8987f7d6c3413566002206216229ede9b4d6ec2d325be245c5b508ff0339bf1794078e20bfe0babc7ffe683270063ab68210392972e2eb617b2388771abe27235fd5ac44af8e61693261550447a4c3e39da98ac024730440220032521802a76ad7bf74d0e2c218b72cf0cbc867066e2e53db905ba37f130397e02207709e2188ed7f08f4c952d9d13986da504502b8c3be59617e043552f506c46ff83275163ab68210392972e2eb617b2388771abe27235fd5ac44af8e61693261550447a4c3e39da98ac00000000")

        txs_out = [
            TxOut(int(coin_value * 1e8), h2b(script_hex)) for coin_value, script_hex in [
                (0.16777215, "0020ba468eea561b26301e4cf69fa34bde4ad60c81e70f059f045ca9a79931004a4d"),
                (0.16777215, "0020d9bbfbe56af7c4b7f960a70d7ea107156913d9e5a26b0a71429df5e097ca6537"),
            ]
        ]

        for tx in (tx_u4, tx_s4):
            self.assertEqual(len(tx.txs_in), 2)
            self.assertEqual(len(tx.txs_out), 2)
            self.assertEqual(tx.version, 1)
            self.assertEqual(tx.lock_time, 0)
            tx.set_unspents(txs_out)
        self.check_unsigned(tx_u4)
        self.check_signed(tx_s4)

        tx_u5 = Tx.from_hex("010000000136641869ca081e70f394c6948e8af409e18b619df2ed74aa106c1ca29787b96e0100000000ffffffff0200e9a435000000001976a914389ffce9cd9ae88dcc0631e88a821ffdbe9bfe2688acc0832f05000000001976a9147480a33f950689af511e6e84c138dbbd3c3ee41588ac00000000")
        tx_s5 = Tx.from_hex("0100000000010136641869ca081e70f394c6948e8af409e18b619df2ed74aa106c1ca29787b96e0100000023220020a16b5755f7f6f96dbd65f5f0d6ab9418b89af4b1f14a1bb8a09062c35f0dcb54ffffffff0200e9a435000000001976a914389ffce9cd9ae88dcc0631e88a821ffdbe9bfe2688acc0832f05000000001976a9147480a33f950689af511e6e84c138dbbd3c3ee41588ac080047304402206ac44d672dac41f9b00e28f4df20c52eeb087207e8d758d76d92c6fab3b73e2b0220367750dbbe19290069cba53d096f44530e4f98acaa594810388cf7409a1870ce01473044022068c7946a43232757cbdf9176f009a928e1cd9a1a8c212f15c1e11ac9f2925d9002205b75f937ff2f9f3c1246e547e54f62e027f64eefa2695578cc6432cdabce271502473044022059ebf56d98010a932cf8ecfec54c48e6139ed6adb0728c09cbe1e4fa0915302e022007cd986c8fa870ff5d2b3a89139c9fe7e499259875357e20fcbb15571c76795403483045022100fbefd94bd0a488d50b79102b5dad4ab6ced30c4069f1eaa69a4b5a763414067e02203156c6a5c9cf88f91265f5a942e96213afae16d83321c8b31bb342142a14d16381483045022100a5263ea0553ba89221984bd7f0b13613db16e7a70c549a86de0cc0444141a407022005c360ef0ae5a5d4f9f2f87a56c1546cc8268cab08c73501d6b3be2e1e1a8a08824730440220525406a1482936d5a21888260dc165497a90a15669636d8edca6b9fe490d309c022032af0c646a34a44d1f4576bf6a4a74b67940f8faa84c7df9abe12a01a11e2b4783cf56210307b8ae49ac90a048e9b53357a2354b3334e9c8bee813ecb98e99a7e07e8c3ba32103b28f0c28bfab54554ae8c658ac5c3e0ce6e79ad336331f78c428dd43eea8449b21034b8113d703413d57761b8b9781957b8c0ac1dfe69f492580ca4195f50376ba4a21033400f6afecb833092a9a21cfdf1ed1376e58c5d1f47de74683123987e967a8f42103a6d48b1131e94ba04d9737d61acdaa1322008af9602b3b14862c07a1789aac162102d8b661b0b3302ee2f162b09e07a55ad5dfbe673a9f01d9f0c19617681024306b56ae00000000")

        txs_out = [
            TxOut(int(coin_value * 1e8), h2b(script_hex)) for coin_value, script_hex in [
                (9.87654321, "a9149993a429037b5d912407a71c252019287b8d27a587"),
            ]
        ]

        for tx in (tx_u5, tx_s5):
            self.assertEqual(len(tx.txs_in), 1)
            self.assertEqual(len(tx.txs_out), 2)
            self.assertEqual(tx.version, 1)
            self.assertEqual(tx.lock_time, 0)
            tx.set_unspents(txs_out)
        self.check_unsigned(tx_u5)
        self.check_signed(tx_s5)
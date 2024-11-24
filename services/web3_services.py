import dotenv
from tonutils.client import TonapiClient
from tonutils.wallet import WalletV4R2
from tonutils.jetton import JettonMaster, JettonWallet
from pytoniq_core import Address, begin_cell
import os


class Web3Service:
    def __init__(self):
        # Initialize TON client
        dotenv.load_dotenv()
        self.client = TonapiClient(api_key=os.getenv("API_KEY"), is_testnet=True)
        self.contract_address = "kQDTQgP1605MG0pbowAuSTb5K1vjd4eMQJMtftjqspIHlpMj"

        # Load wallet from seed phrase (you can customize how to retrieve this securely)
        mnemonics = os.getenv("MNEMONICS").split(",") if os.getenv("MNEMONICS") else []
        if not mnemonics:
            raise ValueError("MNEMONICS environment variable not found.")
        self.wallet, self.public_key, self.private_key, self.mnemonic = WalletV4R2.from_mnemonic(client=self.client,
                                                                                                 mnemonic=mnemonics)

    async def claim(self, recipient_address, amount):
        try:
            COMMENT = "Claimed Tokens"
            JETTON_DECIMALS = 9

            body = JettonWallet.build_transfer_body(
                recipient_address=Address(recipient_address),
                response_address=self.wallet.address,
                jetton_amount=int(amount * (10 ** JETTON_DECIMALS)),
                forward_payload=(
                    begin_cell()
                    .store_uint(0, 32)  # Text comment opcode
                    .store_snake_string(COMMENT)
                    .end_cell()
                ),
                forward_amount=1,
            )
            # Transfer tokens to the recipient address
            tx_hash = await self.wallet.transfer(
                destination=Address("kQDTQgP1605MG0pbowAuSTb5K1vjd4eMQJMtftjqspIHlpMj"),
                amount=0.05,
                body=body,
            )
            return tx_hash  # Optionally return transaction info
        except Exception as e:
            return {'error': str(e)}

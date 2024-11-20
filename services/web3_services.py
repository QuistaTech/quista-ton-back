import dotenv
from tonutils.client import TonapiClient
from tonutils.wallet import WalletV4R2
import os


class Web3Service:
    def __init__(self):
        # Initialize TON client
        dotenv.load_dotenv()
        self.client = TonapiClient(api_key=os.getenv("API_KEY"), is_testnet=True)

        # Load wallet from seed phrase (you can customize how to retrieve this securely)
        mnemonics = os.getenv("MNEMONICS").split(",") if os.getenv("MNEMONICS") else []
        if not mnemonics:
            raise ValueError("MNEMONICS environment variable not found.")
        self.wallet, self.public_key, self.private_key, self.mnemonic = WalletV4R2.from_mnemonic(client=self.client,
                                                                                                 mnemonic=mnemonics)

    async def claim(self, recipient_address, amount):
        try:
            # Transfer tokens to the recipient address
            transaction = await self.wallet.transfer(
                destination=recipient_address,
                amount=float(amount),  # This amount should be in nanograms (1 TON = 1,000,000,000 nanograms)
            )
            return transaction  # Optionally return transaction info
        except Exception as e:
            return {'error': str(e)}

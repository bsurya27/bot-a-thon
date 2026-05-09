import json, os, base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

os.makedirs('.agent', exist_ok=True)

private_key = Ed25519PrivateKey.generate()
private_bytes = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
public_bytes = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)

with open('.agent/keypair.json', 'w') as f:
    json.dump({
        'private_key': base64.b64encode(private_bytes).decode(),
        'public_key': base64.b64encode(public_bytes).decode()
    }, f, indent=2)

print('✅ Done')
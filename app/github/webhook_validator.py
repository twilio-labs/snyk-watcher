import hmac
import hashlib

from app.common.logging import getLogger

logger = getLogger(__name__)


# Get sha1 hmac from payload and secret.
def sign_payload(payload: str, secret: str) -> bool:
    key = bytes(secret, 'utf-8')
    mac = hmac.new(key, msg=payload, digestmod=hashlib.sha1)

    return mac.hexdigest()


# Helper method to parse passed webhook signature.
def extract_signature(signature: str) -> str:
    if not signature or 'sha1' not in signature or '=' not in signature:
        return ''

    return signature.split('=')[-1]


# Compare sent hash vs calculated hash.
def verify_webhook(payload: str, signature: str, secret: str) -> bool:
    signature_hash = extract_signature(signature)
    calculated_hash = sign_payload(payload, secret)

    if not signature_hash:
        logger.error('Invalid signature format provided.')
        return False

    if not hmac.compare_digest(signature_hash, calculated_hash):
        logger.error('Invalid signature provided.')
        return False

    return True

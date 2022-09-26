import base64
import binascii
from enum import Enum
import json
import os
import string
from typing import Optional

from pydantic import BaseModel, Field, SecretStr, validator

from .utils import address_from_pubkey, create_new_ppk, priv_key_from_ppk

PKG_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
LOGO_PATH = os.path.join(PKG_DIR, "assets", "POKT_symbol_bg.png")


class ImplementedKDFs(str, Enum):
    scrypt = "scrypt"


class PPK(BaseModel):
    class Config:
        use_enum_values = True

    kdf: ImplementedKDFs = Field(
        ..., description="Currently only scrypt is implemented"
    )
    salt: str = Field(..., description="Cannot be empty, and can be decoded from hex")
    secparam: int = Field(
        ...,
        description="The cost, and the value that determines how many bytes are used to determine the nonce.",
    )
    hint: Optional[str] = Field(
        "", description="An optional hint for the password used to encrypt"
    )
    ciphertext: str = Field(..., description="Can be decoded from base64.")
    pub_key: Optional[str] = Field(
        None, description="The public key of the associated PPK"
    )

    @classmethod
    def new(cls, passphrase: str, hint: Optional[str] = None, secparam: int = 12):
        return create_new_ppk(passphrase, hint=hint, secparam=secparam)

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, "r") as kf:
            data = json.load(kf)
        return cls(**data)

    @property
    def salt_bytes(self) -> bytes:
        return bytes.fromhex(self.salt)

    @property
    def address(self) -> str:
        if self.pub_key is None:
            return "Unknown"
        return address_from_pubkey(self.pub_key)

    @property
    def ciphertext_bytes(self) -> bytes:
        return base64.b64decode(self.ciphertext)

    @validator("salt")
    def salt_cannot_be_empty(cls, v):
        if not v:
            raise ValueError("The value for salt cannot be empty.")
        return v

    @validator("salt")
    def salt_must_be_hex_decodable(cls, v):
        if not all(c in string.hexdigits for c in v):
            raise ValueError("The value for salt cannot be hex decoded.")
        return v

    @validator("ciphertext")
    def ciphertext_must_be_base64_decoable(cls, v):
        try:
            base64.b64decode(v, validate=True)
        except binascii.Error:
            raise ValueError("The value for ciphertext cannot be base64 decoded.")
        return v

    def unlock(self, password: str):
        priv_key = priv_key_from_ppk(self, password)
        if self.pub_key is None:
            self.pub_key = priv_key[64:]
        return UnlockedPPK(priv_key=priv_key, **self.dict())

    def _make_qr_image(self):
        try:
            import qrcode
            from qrcode.image.styledpil import StyledPilImage
            from qrcode.image.styles.colormasks import SolidFillColorMask
            from qrcode.image.styles.moduledrawers import CircleModuleDrawer
        except:
            raise ImportError(
                "Required dependencies qrcode and Pillow not installed. To install the needed dependencies to render a QR code image, run `pip install pypokt[all]`"
            )
        if self.pub_key is None:
            raise RuntimeError(
                "QR Code cannot be created for PPK with unknown pub_key. If this PPK was loaded from a file, it must be unlocked to determine it's corresponding public key."
            )
        qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_H)
        qr.add_data(self.address)

        qr_color = SolidFillColorMask(
            front_color=(29, 138, 237), back_color=(255, 255, 255)
        )
        return qr.make_image(
            image_factory=StyledPilImage,
            embeded_image_path=LOGO_PATH,
            module_drawer=CircleModuleDrawer(),
            color_mask=qr_color,
        ).convert("RGBA")

    def _as_str(self):
        base = "PPK({})".format(self)
        if self.pub_key is None:
            base += (
                "\nNote: Imported PPK. Public key and address unknown until unlocked."
            )
        return base

    def _ipython_display_(self):
        from IPython import display

        print("{}".format(self._as_str()))
        if self.pub_key is None:
            return
        try:
            img = self._make_qr_image()
        except ImportError:
            pass
        else:
            display.display(display.Image(img._repr_png_()))
        finally:
            print("Address: {}".format(self.address))


class UnlockedPPK(PPK):
    priv_key: SecretStr

    @property
    def private_key(self):
        return self.priv_key.get_secret_value()

from __future__ import annotations

import json
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel

from google.protobuf.any_pb2 import Any as ProtoAny


class Base(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True

    @classmethod
    def from_json(cls, filename: str):
        with open(filename, "r") as f:
            data = json.load(f)
            return cls(**data)


class ProtobufTypes(int, Enum):
    DOUBLE = 1
    FLOAT = 2
    INT64 = 3
    UINT64 = 4
    INT32 = 5
    FIXED64 = 6
    FIXED32 = 7
    BOOL = 8
    STRING = 9
    GROUP = 10
    MESSAGE = 11
    BYTES = 12
    UINT32 = 13
    ENUM = 14
    SFIXED32 = 15
    SFIXED64 = 16
    SINT32 = 17
    SINT64 = 18
    ANY = 19


def encode_proto_type(
    value: Any, proto_type: Optional[ProtobufTypes] = None, repeats: bool = False
):
    if repeats:
        return [encode_proto_type(item, proto_type) for item in value]
    if proto_type in (
        None,
        ProtobufTypes.FIXED32,
        ProtobufTypes.FIXED64,
        ProtobufTypes.SFIXED32,
        ProtobufTypes.SFIXED64,
        ProtobufTypes.GROUP,
    ):
        return value
    elif proto_type in (ProtobufTypes.MESSAGE,):
        if isinstance(value, ProtobufBase):
            return value.protobuf_message()
        return value
    elif proto_type in (ProtobufTypes.ANY,):
        msg = ProtoAny()
        msg.Pack(value.protobuf_message())
        return msg
    elif proto_type in (ProtobufTypes.DOUBLE, ProtobufTypes.FLOAT):
        return float(value)
    elif proto_type in (
        ProtobufTypes.INT64,
        ProtobufTypes.UINT64,
        ProtobufTypes.INT32,
        ProtobufTypes.UINT32,
        ProtobufTypes.SINT32,
        ProtobufTypes.SINT64,
    ):
        return int(value)
    elif proto_type in (ProtobufTypes.BYTES,):
        return bytes(value, "utf-8")
    elif proto_type in (ProtobufTypes.BOOL,):
        return bool(value)
    elif proto_type in (ProtobufTypes.STRING, ProtobufTypes.ENUM):
        return str(value)
    elif issubclass(value, ProtobufBase):
        return value


class ProtobufBase(Base):

    __protobuf_model__: Any = None

    @classmethod
    def __proto_fields__(cls):
        proto_fields = {}
        for name, val in cls.__fields__.items():
            proto_name = val.field_info.extra.get("proto_name", name)
            proto_type = val.field_info.extra.get("proto_type")

            proto_repeated = val.field_info.extra.get("proto_repeated", False)
            proto_fields[name] = (proto_name, proto_type, proto_repeated)

        return proto_fields

    def protobuf_message(self):
        if self.__protobuf_model__ is None:
            raise ValueError("The protobuf model was never defined.")
        msg = self.__protobuf_model__()
        proto_fields = self.__proto_fields__()
        for name, (proto_name, field_type, repeats) in proto_fields.items():
            value = getattr(self, name)
            try:
                if repeats:
                    getattr(msg, proto_name).extend(
                        encode_proto_type(value, field_type, repeats)
                    )
                elif field_type in (ProtobufTypes.MESSAGE, ProtobufTypes.ANY):
                    getattr(msg, proto_name).CopyFrom(
                        encode_proto_type(value, field_type, repeats)
                    )
                else:
                    setattr(
                        msg, proto_name, encode_proto_type(value, field_type, repeats)
                    )
            except TypeError:
                ft = field_type.value if field_type is not None else "None"
                raise TypeError(
                    "Type error occurred when encoding {} to {} for field {}".format(
                        value, ft, proto_name
                    )
                )
        return msg

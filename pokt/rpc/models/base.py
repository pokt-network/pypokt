from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel

class Base(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True

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

def encode_proto_type(value: Any, proto_type: Optional[ProtobufTypes] = None):
    if proto_type in (
        None,
        ProtobufTypes.FIXED32,
        ProtobufTypes.FIXED64,
        ProtobufTypes.SFIXED32,
        ProtobufTypes.SFIXED64,
        ProtobufTypes.MESSAGE,
        ProtobufTypes.GROUP,
    ):
        return value
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
            proto_fields[name] = (proto_name, proto_type)

        return proto_fields

    def protobuf_payload(self):
        if self.__protobuf_model__ is None:
            raise ValueError("The protobuf model was never defined.")
        msg = self.__protobuf_model__()
        proto_fields = self.__proto_fields__()
        for name, (proto_name, field_type) in proto_fields.items():
            value = getattr(self, name)
            try:
                setattr(msg, proto_name, encode_proto_type(value, field_type))
            except TypeError:
                ft = field_type.value if field_type is not None else "None"
                raise TypeError(
                    "Type error occurred when encoding {} to {} for field {}".format(
                        value, ft, proto_name
                    )
                )
        return msg.SerializeToString()

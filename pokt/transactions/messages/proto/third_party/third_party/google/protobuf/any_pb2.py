# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: third_party/google/protobuf/any.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n%third_party/google/protobuf/any.proto\x12\x0fgoogle.protobuf"&\n\x03\x41ny\x12\x10\n\x08type_url\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x42v\n\x13\x63om.google.protobufB\x08\x41nyProtoP\x01Z,google.golang.org/protobuf/types/known/anypb\xa2\x02\x03GPB\xaa\x02\x1eGoogle.Protobuf.WellKnownTypesb\x06proto3'
)


_ANY = DESCRIPTOR.message_types_by_name["Any"]
Any = _reflection.GeneratedProtocolMessageType(
    "Any",
    (_message.Message,),
    {
        "DESCRIPTOR": _ANY,
        "__module__": "third_party.google.protobuf.any_pb2"
        # @@protoc_insertion_point(class_scope:google.protobuf.Any)
    },
)
_sym_db.RegisterMessage(Any)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\023com.google.protobufB\010AnyProtoP\001Z,google.golang.org/protobuf/types/known/anypb\242\002\003GPB\252\002\036Google.Protobuf.WellKnownTypes"
    _ANY._serialized_start = 58
    _ANY._serialized_end = 96
# @@protoc_insertion_point(module_scope)

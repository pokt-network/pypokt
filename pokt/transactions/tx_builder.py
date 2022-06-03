from pokt.rpc.models import MsgSendVal, ProtobufTypes
from .messages.proto import tx_signer_pb2 as proto


def protobuf_inspect(model, indent=""):
    for name, desc in model.DESCRIPTOR.fields_by_name.items():
        if desc.message_type:
            print("{}{} {}".format(indent, name, desc.message_type.name))
            other_proto_inst = getattr(proto, desc.message_type.name, None)
            if other_proto_inst:
                protobuf_inspect(other_proto_inst, indent=indent + "  ")
        else:
            print("{}{} {}".format(indent, name, ProtobufTypes(desc.type).name))


def build_tx():
    protobuf_inspect(proto.ProtoStdTx)


def build_send_tx_msg(from_address: str, to_address: str, amount: int):
    msg = MsgSendVal(from_address=from_address, to_address=to_address, amount=amount)
    print(msg.protobuf_payload())

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: contract_processed.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="contract_processed.proto",
    package="",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x18\x63ontract_processed.proto"o\n\x11\x43ontractProcessed\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x19\n\x11\x63reated_timestamp\x18\x03 \x01(\x03\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x10\n\x08is_token\x18\x05 \x01(\x08\x62\x06proto3'
    ),
)


_CONTRACTPROCESSED = _descriptor.Descriptor(
    name="ContractProcessed",
    full_name="ContractProcessed",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="address",
            full_name="ContractProcessed.address",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="name",
            full_name="ContractProcessed.name",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="created_timestamp",
            full_name="ContractProcessed.created_timestamp",
            index=2,
            number=3,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="status",
            full_name="ContractProcessed.status",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="is_token",
            full_name="ContractProcessed.is_token",
            index=4,
            number=5,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=28,
    serialized_end=139,
)

DESCRIPTOR.message_types_by_name["ContractProcessed"] = _CONTRACTPROCESSED
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ContractProcessed = _reflection.GeneratedProtocolMessageType(
    "ContractProcessed",
    (_message.Message,),
    dict(
        DESCRIPTOR=_CONTRACTPROCESSED,
        __module__="contract_processed_pb2"
        # @@protoc_insertion_point(class_scope:ContractProcessed)
    ),
)
_sym_db.RegisterMessage(ContractProcessed)


# @@protoc_insertion_point(module_scope)

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Login.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Login.proto',
  package='',
  serialized_pb=_b('\n\x0bLogin.proto\"\x19\n\x05Login\x12\x10\n\x08UserName\x18\x01 \x02(\t\"!\n\x08LoginReq\x12\x15\n\x05login\x18\x01 \x02(\x0b\x32\x06.Login\"+\n\x08LoginRes\x12\x0f\n\x07msgCode\x18\x01 \x02(\x05\x12\x0e\n\x06userId\x18\x02 \x02(\x05')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_LOGIN = _descriptor.Descriptor(
  name='Login',
  full_name='Login',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='UserName', full_name='Login.UserName', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=40,
)


_LOGINREQ = _descriptor.Descriptor(
  name='LoginReq',
  full_name='LoginReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='login', full_name='LoginReq.login', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=75,
)


_LOGINRES = _descriptor.Descriptor(
  name='LoginRes',
  full_name='LoginRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgCode', full_name='LoginRes.msgCode', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='userId', full_name='LoginRes.userId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=120,
)

_LOGINREQ.fields_by_name['login'].message_type = _LOGIN
DESCRIPTOR.message_types_by_name['Login'] = _LOGIN
DESCRIPTOR.message_types_by_name['LoginReq'] = _LOGINREQ
DESCRIPTOR.message_types_by_name['LoginRes'] = _LOGINRES

Login = _reflection.GeneratedProtocolMessageType('Login', (_message.Message,), dict(
  DESCRIPTOR = _LOGIN,
  __module__ = 'Login_pb2'
  # @@protoc_insertion_point(class_scope:Login)
  ))
_sym_db.RegisterMessage(Login)

LoginReq = _reflection.GeneratedProtocolMessageType('LoginReq', (_message.Message,), dict(
  DESCRIPTOR = _LOGINREQ,
  __module__ = 'Login_pb2'
  # @@protoc_insertion_point(class_scope:LoginReq)
  ))
_sym_db.RegisterMessage(LoginReq)

LoginRes = _reflection.GeneratedProtocolMessageType('LoginRes', (_message.Message,), dict(
  DESCRIPTOR = _LOGINRES,
  __module__ = 'Login_pb2'
  # @@protoc_insertion_point(class_scope:LoginRes)
  ))
_sym_db.RegisterMessage(LoginRes)


# @@protoc_insertion_point(module_scope)

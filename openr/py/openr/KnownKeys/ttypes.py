#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#  @generated
#

from __future__ import absolute_import
import six
from thrift.util.Recursive import fix_spec
from thrift.Thrift import *
from thrift.protocol.TProtocol import TProtocolException



import pprint
import warnings
from thrift import Thrift
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
from thrift.protocol import THeaderProtocol
try:
  from thrift.protocol import fastproto
except:
  fastproto = None
all_structs = []
UTF8STRINGS = bool(0) or sys.version_info.major >= 3

__all__ = ['UTF8STRINGS', 'KnownKeys', 'CurveKeyPair']

class KnownKeys:
  """
  Attributes:
   - keys
  """

  thrift_spec = None
  thrift_field_annotations = None
  thrift_struct_annotations = None
  __init__ = None
  @staticmethod
  def isUnion():
    return False

  def read(self, iprot):
    if (isinstance(iprot, TBinaryProtocol.TBinaryProtocolAccelerated) or (isinstance(iprot, THeaderProtocol.THeaderProtocolAccelerate) and iprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_BINARY_PROTOCOL)) and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastproto is not None:
      fastproto.decode(self, iprot.trans, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=0)
      self.checkRequired()
      return
    if (isinstance(iprot, TCompactProtocol.TCompactProtocolAccelerated) or (isinstance(iprot, THeaderProtocol.THeaderProtocolAccelerate) and iprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_COMPACT_PROTOCOL)) and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastproto is not None:
      fastproto.decode(self, iprot.trans, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=2)
      self.checkRequired()
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.MAP:
          self.keys = {}
          (_ktype1, _vtype2, _size0 ) = iprot.readMapBegin() 
          if _size0 >= 0:
            for _i4 in six.moves.range(_size0):
              _key5 = iprot.readString().decode('utf-8') if UTF8STRINGS else iprot.readString()
              _val6 = iprot.readString()
              self.keys[_key5] = _val6
          else: 
            while iprot.peekMap():
              _key7 = iprot.readString().decode('utf-8') if UTF8STRINGS else iprot.readString()
              _val8 = iprot.readString()
              self.keys[_key7] = _val8
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()
    self.checkRequired()

  def checkRequired(self):
    if self.keys == None:
      raise TProtocolException(TProtocolException.MISSING_REQUIRED_FIELD, "Required field 'keys' was not found in serialized data! Struct: KnownKeys")

    return

  def write(self, oprot):
    if (isinstance(oprot, TBinaryProtocol.TBinaryProtocolAccelerated) or (isinstance(oprot, THeaderProtocol.THeaderProtocolAccelerate) and oprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_BINARY_PROTOCOL)) and self.thrift_spec is not None and fastproto is not None:
      oprot.trans.write(fastproto.encode(self, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=0))
      return
    if (isinstance(oprot, TCompactProtocol.TCompactProtocolAccelerated) or (isinstance(oprot, THeaderProtocol.THeaderProtocolAccelerate) and oprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_COMPACT_PROTOCOL)) and self.thrift_spec is not None and fastproto is not None:
      oprot.trans.write(fastproto.encode(self, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=2))
      return
    oprot.writeStructBegin('KnownKeys')
    if self.keys != None:
      oprot.writeFieldBegin('keys', TType.MAP, 1)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.keys))
      for kiter9,viter10 in self.keys.items():
        oprot.writeString(kiter9.encode('utf-8')) if UTF8STRINGS and not isinstance(kiter9, bytes) else oprot.writeString(kiter9)
        oprot.writeString(viter10)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def __repr__(self):
    L = []
    padding = ' ' * 4
    value = pprint.pformat(self.keys, indent=0)
    value = padding.join(value.splitlines(True))
    L.append('    keys=%s' % (value))
    return "%s(\n%s)" % (self.__class__.__name__, ",\n".join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False

    return self.__dict__ == other.__dict__ 

  def __ne__(self, other):
    return not (self == other)

  # Override the __hash__ function for Python3 - t10434117
  if not six.PY2:
    __hash__ = object.__hash__

class CurveKeyPair:
  """
  Attributes:
   - privateKey
   - publicKey
  """

  thrift_spec = None
  thrift_field_annotations = None
  thrift_struct_annotations = None
  __init__ = None
  @staticmethod
  def isUnion():
    return False

  def read(self, iprot):
    if (isinstance(iprot, TBinaryProtocol.TBinaryProtocolAccelerated) or (isinstance(iprot, THeaderProtocol.THeaderProtocolAccelerate) and iprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_BINARY_PROTOCOL)) and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastproto is not None:
      fastproto.decode(self, iprot.trans, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=0)
      self.checkRequired()
      return
    if (isinstance(iprot, TCompactProtocol.TCompactProtocolAccelerated) or (isinstance(iprot, THeaderProtocol.THeaderProtocolAccelerate) and iprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_COMPACT_PROTOCOL)) and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastproto is not None:
      fastproto.decode(self, iprot.trans, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=2)
      self.checkRequired()
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.privateKey = iprot.readString()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.publicKey = iprot.readString()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()
    self.checkRequired()

  def checkRequired(self):
    return

  def write(self, oprot):
    if (isinstance(oprot, TBinaryProtocol.TBinaryProtocolAccelerated) or (isinstance(oprot, THeaderProtocol.THeaderProtocolAccelerate) and oprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_BINARY_PROTOCOL)) and self.thrift_spec is not None and fastproto is not None:
      oprot.trans.write(fastproto.encode(self, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=0))
      return
    if (isinstance(oprot, TCompactProtocol.TCompactProtocolAccelerated) or (isinstance(oprot, THeaderProtocol.THeaderProtocolAccelerate) and oprot.get_protocol_id() == THeaderProtocol.THeaderProtocol.T_COMPACT_PROTOCOL)) and self.thrift_spec is not None and fastproto is not None:
      oprot.trans.write(fastproto.encode(self, [self.__class__, self.thrift_spec, False], utf8strings=UTF8STRINGS, protoid=2))
      return
    oprot.writeStructBegin('CurveKeyPair')
    if self.privateKey != None:
      oprot.writeFieldBegin('privateKey', TType.STRING, 1)
      oprot.writeString(self.privateKey)
      oprot.writeFieldEnd()
    if self.publicKey != None:
      oprot.writeFieldBegin('publicKey', TType.STRING, 2)
      oprot.writeString(self.publicKey)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def __repr__(self):
    L = []
    padding = ' ' * 4
    value = pprint.pformat(self.privateKey, indent=0)
    value = padding.join(value.splitlines(True))
    L.append('    privateKey=%s' % (value))
    value = pprint.pformat(self.publicKey, indent=0)
    value = padding.join(value.splitlines(True))
    L.append('    publicKey=%s' % (value))
    return "%s(\n%s)" % (self.__class__.__name__, ",\n".join(L))

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False

    return self.__dict__ == other.__dict__ 

  def __ne__(self, other):
    return not (self == other)

  # Override the __hash__ function for Python3 - t10434117
  if not six.PY2:
    __hash__ = object.__hash__

all_structs.append(KnownKeys)
KnownKeys.thrift_spec = (
  None, # 0
  (1, TType.MAP, 'keys', (TType.STRING,True,TType.STRING,False), None, 0, ), # 1
)

KnownKeys.thrift_struct_annotations = {
}
KnownKeys.thrift_field_annotations = {
}

def KnownKeys__init__(self, keys=None,):
  self.keys = keys

KnownKeys.__init__ = KnownKeys__init__

all_structs.append(CurveKeyPair)
CurveKeyPair.thrift_spec = (
  None, # 0
  (1, TType.STRING, 'privateKey', False, None, 2, ), # 1
  (2, TType.STRING, 'publicKey', False, None, 2, ), # 2
)

CurveKeyPair.thrift_struct_annotations = {
}
CurveKeyPair.thrift_field_annotations = {
}

def CurveKeyPair__init__(self, privateKey=None, publicKey=None,):
  self.privateKey = privateKey
  self.publicKey = publicKey

CurveKeyPair.__init__ = CurveKeyPair__init__

fix_spec(all_structs)
del all_structs

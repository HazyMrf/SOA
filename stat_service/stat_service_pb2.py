# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stat_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12stat_service.proto\x12\x0bstatservice\x1a\x1bgoogle/protobuf/empty.proto\"(\n\x15PostStatisticsRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x04\"6\n\x16PostStatisticsResponse\x12\r\n\x05likes\x18\x01 \x01(\x04\x12\r\n\x05views\x18\x02 \x01(\x04\"(\n\x0fTopPostsRequest\x12\x15\n\rsort_by_likes\x18\x01 \x01(\x08\")\n\x07TopPost\x12\x0f\n\x07post_id\x18\x01 \x01(\x04\x12\r\n\x05score\x18\x02 \x01(\x04\"7\n\x10TopPostsResponse\x12#\n\x05posts\x18\x01 \x03(\x0b\x32\x14.statservice.TopPost\"+\n\x0eUserStatistics\x12\n\n\x02id\x18\x01 \x01(\x04\x12\r\n\x05likes\x18\x02 \x01(\x04\">\n\x10TopUsersResponse\x12*\n\x05users\x18\x01 \x03(\x0b\x32\x1b.statservice.UserStatistics2\x83\x02\n\x0bStatService\x12^\n\x11GetPostStatistics\x12\".statservice.PostStatisticsRequest\x1a#.statservice.PostStatisticsResponse\"\x00\x12L\n\x0bGetTopPosts\x12\x1c.statservice.TopPostsRequest\x1a\x1d.statservice.TopPostsResponse\"\x00\x12\x46\n\x0bGetTopUsers\x12\x16.google.protobuf.Empty\x1a\x1d.statservice.TopUsersResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stat_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_POSTSTATISTICSREQUEST']._serialized_start=64
  _globals['_POSTSTATISTICSREQUEST']._serialized_end=104
  _globals['_POSTSTATISTICSRESPONSE']._serialized_start=106
  _globals['_POSTSTATISTICSRESPONSE']._serialized_end=160
  _globals['_TOPPOSTSREQUEST']._serialized_start=162
  _globals['_TOPPOSTSREQUEST']._serialized_end=202
  _globals['_TOPPOST']._serialized_start=204
  _globals['_TOPPOST']._serialized_end=245
  _globals['_TOPPOSTSRESPONSE']._serialized_start=247
  _globals['_TOPPOSTSRESPONSE']._serialized_end=302
  _globals['_USERSTATISTICS']._serialized_start=304
  _globals['_USERSTATISTICS']._serialized_end=347
  _globals['_TOPUSERSRESPONSE']._serialized_start=349
  _globals['_TOPUSERSRESPONSE']._serialized_end=411
  _globals['_STATSERVICE']._serialized_start=414
  _globals['_STATSERVICE']._serialized_end=673
# @@protoc_insertion_point(module_scope)

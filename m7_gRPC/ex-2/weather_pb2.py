# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: weather.proto
# Protobuf Python Version: 6.31.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    1,
    '',
    'weather.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rweather.proto\x12\x07weather\"1\n\x0b\x43ityRequest\x12\x0c\n\x04\x63ity\x18\x01 \x01(\t\x12\x14\n\x0c\x63ountry_code\x18\x02 \x01(\t\"C\n\x0f\x46orecastRequest\x12\x0c\n\x04\x63ity\x18\x01 \x01(\t\x12\x14\n\x0c\x63ountry_code\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ys\x18\x03 \x01(\x05\"\xa5\x01\n\x0fWeatherResponse\x12\x0c\n\x04\x63ity\x18\x01 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x02 \x01(\t\x12\x13\n\x0btemperature\x18\x03 \x01(\x01\x12\x12\n\nfeels_like\x18\x04 \x01(\x01\x12\x10\n\x08humidity\x18\x05 \x01(\x01\x12\x12\n\nwind_speed\x18\x06 \x01(\x01\x12\x11\n\tcondition\x18\x07 \x01(\t\x12\x11\n\ttimestamp\x18\x08 \x01(\x03\"\x98\x01\n\rDailyForecast\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\x03\x12\x10\n\x08temp_min\x18\x02 \x01(\x01\x12\x10\n\x08temp_max\x18\x03 \x01(\x01\x12\x10\n\x08humidity\x18\x04 \x01(\x01\x12\x12\n\nwind_speed\x18\x05 \x01(\x01\x12\x11\n\tcondition\x18\x06 \x01(\t\x12\x1c\n\x14precipitation_chance\x18\x07 \x01(\x01\"X\n\x10\x46orecastResponse\x12\x0c\n\x04\x63ity\x18\x01 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x02 \x01(\t\x12%\n\x05\x64\x61ily\x18\x03 \x03(\x0b\x32\x16.weather.DailyForecast\"\xd0\x01\n\x0bWeatherData\x12\x12\n\nstation_id\x18\x01 \x01(\t\x12\x10\n\x08latitude\x18\x02 \x01(\x01\x12\x11\n\tlongitude\x18\x03 \x01(\x01\x12\x13\n\x0btemperature\x18\x04 \x01(\x01\x12\x10\n\x08humidity\x18\x05 \x01(\x01\x12\x10\n\x08pressure\x18\x06 \x01(\x01\x12\x12\n\nwind_speed\x18\x07 \x01(\x01\x12\x16\n\x0ewind_direction\x18\x08 \x01(\x01\x12\x10\n\x08rainfall\x18\t \x01(\x01\x12\x11\n\ttimestamp\x18\n \x01(\x03\"K\n\x0c\x44\x61taResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x19\n\x11records_processed\x18\x03 \x01(\x05\"\\\n\x0b\x43hatMessage\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x18\n\x10is_meteorologist\x18\x04 \x01(\x08\x32\xfd\x02\n\x0eWeatherService\x12\x45\n\x11GetCurrentWeather\x12\x14.weather.CityRequest\x1a\x18.weather.WeatherResponse\"\x00\x12\x44\n\x0bGetForecast\x12\x18.weather.ForecastRequest\x1a\x19.weather.ForecastResponse\"\x00\x12O\n\x19SubscribeToWeatherUpdates\x12\x14.weather.CityRequest\x1a\x18.weather.WeatherResponse\"\x00\x30\x01\x12\x42\n\x0fSendWeatherData\x12\x14.weather.WeatherData\x1a\x15.weather.DataResponse\"\x00(\x01\x12I\n\x15\x43hatWithMeteorologist\x12\x14.weather.ChatMessage\x1a\x14.weather.ChatMessage\"\x00(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'weather_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CITYREQUEST']._serialized_start=26
  _globals['_CITYREQUEST']._serialized_end=75
  _globals['_FORECASTREQUEST']._serialized_start=77
  _globals['_FORECASTREQUEST']._serialized_end=144
  _globals['_WEATHERRESPONSE']._serialized_start=147
  _globals['_WEATHERRESPONSE']._serialized_end=312
  _globals['_DAILYFORECAST']._serialized_start=315
  _globals['_DAILYFORECAST']._serialized_end=467
  _globals['_FORECASTRESPONSE']._serialized_start=469
  _globals['_FORECASTRESPONSE']._serialized_end=557
  _globals['_WEATHERDATA']._serialized_start=560
  _globals['_WEATHERDATA']._serialized_end=768
  _globals['_DATARESPONSE']._serialized_start=770
  _globals['_DATARESPONSE']._serialized_end=845
  _globals['_CHATMESSAGE']._serialized_start=847
  _globals['_CHATMESSAGE']._serialized_end=939
  _globals['_WEATHERSERVICE']._serialized_start=942
  _globals['_WEATHERSERVICE']._serialized_end=1323
# @@protoc_insertion_point(module_scope)

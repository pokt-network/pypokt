#!/bin/bash

protoc -I ../proto -I ../proto/third_party --python_out=../pokt/transactions/messages/proto ../proto/tx-signer.proto
protoc -I ../proto -I ../proto/third_party --python_out=../pokt/transactions/messages/proto/third_party ../proto/third_party/google/protobuf/any.proto

#!/bin/bash

protoc -I ../proto -I ../proto/third_party --python_out=../pokt/transactions/messages/encoding/proto ../proto/tx-signer.proto

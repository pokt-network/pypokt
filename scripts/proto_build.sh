#!/bin/bash

protoc -I ../proto -I ../proto/third_party --python_out=../pokt/wallet/encoding/proto ../proto/tx-signer.proto

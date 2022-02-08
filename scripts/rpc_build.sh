#!/bin/sh

datamodel-codegen --input "../spec/rpc-spec.yaml" --aliases "../spec/aliases.json" --output "../pokt/rpc/models/_generated.py"

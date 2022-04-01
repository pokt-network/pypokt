#!/bin/sh

datamodel-codegen --input "../spec/rpc-spec.yaml" --aliases "../spec/aliases.json" --output "../pokt/rpc/models/validation/_generated.py"

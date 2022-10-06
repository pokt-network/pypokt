Any models declared here either:
    - address any discrepancies in the models generated from the rpc.yaml
    - add additional clarification about types that were treated as "any" types
      in the rpc.yaml
    - programatically express constraints and enumerations documented in the
      descriptions of the rpc.yaml

Any types not formally expressed in the rpc.yaml can be identified by models
with a "Literal" type field. Pocket core uses amino encoding, and so some
returned models follow the given pattern:

```json
{
  type: str
  value: Any (but really of type)
}
```

We can express these kinds of types via pydantic (and hence OpenAPI) via
discriminator fields.  How this works, is any models following the above
pattern will define models that represent each of the possible types, with the
type defined on the model as a literal that represents the expected string.
From there, we can define the generic model where the type of type still
remains str, but the type of value becomes a Union of all the types that type
could be. By then specifying type as the discriminator on the value field, this
will allow the expected type to be conditionally parsed based on str given as
the type in the object to validate.

The two main instances of this are ParamValueT and MsgT acting as the Union
types for the protocol parameter values and the messages contained in a
transaction's stdTx field.


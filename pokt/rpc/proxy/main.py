from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi

from .conf import ProxySettings, settings
from .data import router as data_router
from ..data.async_network import async_get_version

app = FastAPI(openapi_url="/v1/openapi.json")

app.include_router(data_router)


@app.get("/v1", tags=["network"])
async def version(conf: ProxySettings = Depends(settings)) -> str:
    return await async_get_version(conf.url)


api_description = """
This is the API definition Pocket Network core RPC calls. Pocket is a distributed network that relays data requests and responses to and from any blockchain system. Pocket verifies all relayed data and proportionally rewards the participating nodes with native cryptographic tokens.

"""


def custom_oas():
    if app.openapi_schema:
        return app.openapi_schema
    oas = get_openapi(
        title="Pocket Network",
        description=api_description,
        version="RC-0.9.0",
        terms_of_service="https://pokt.network/terms/",
        contact={
            "name": "Pocket Network",
            "email": "hola@pokt.network",
            "url": "https://pocket.network",
        },
        license_info={
            "name": "MIT Licnese",
            "url": "https://github.com/pokt-network/pocket-core/LICENSE.md",
        },
        servers=[
            {
                "url": "https://mainnet.gateway.pokt.network/v1/lb/{PortalID}",
                "description": "Pocket Portal",
                "variables": {
                    "PortalID": {
                        "default": "REQUIRED",
                        "description": "Found after registering an app with the Pocket Portal.",
                    }
                },
            },
        ],
        routes=app.routes,
    )
    for path, ops in oas["paths"].items():
        for x in ("get", "post"):
            op = ops.get(x)
            if op:
                oas["paths"][path][x]["responses"] = {
                    k: v for k, v in op["responses"].items() if k != "422"
                }

    app.openapi_schema = oas
    return app.openapi_schema


app.openapi = custom_oas


def main():
    import uvicorn

    uvicorn.run("pokt.rpc.proxy.main:app", port=8080, reload=True)


if __name__ == "__main__":
    main()

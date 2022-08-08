from fastapi import Depends, FastAPI

from .conf import ProxySettings, settings
from .data import router as data_router
from ..data.async_network import async_get_version

api_description = """
This is the API definition Pocket Network core RPC calls. Pocket is a distributed network that relays data requests and responses to and from any blockchain system. Pocket verifies all relayed data and proportionally rewards the participating nodes with native cryptographic tokens.

"""

app = FastAPI(
    title="Pocket Network",
    description=api_description,
    version="RC-0.8.3",
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
    openapi_url="/v1/openapi.json",
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
)
app.include_router(data_router)


@app.get("/v1", tags=["network"])
async def version(conf: ProxySettings = Depends(settings)) -> str:
    return await async_get_version(conf.url)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("pokt.rpc.proxy.main:app", port=8080, reload=True)

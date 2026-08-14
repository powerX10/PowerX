import argparse
import asyncio
import json
import httpx


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8300)
    args = parser.parse_args()

    base = f"http://127.0.0.1:{args.port}/v1"
    async with httpx.AsyncClient(timeout=10) as client:
        models = await client.get(base + "/models")
        models.raise_for_status()
        print(json.dumps(models.json(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())

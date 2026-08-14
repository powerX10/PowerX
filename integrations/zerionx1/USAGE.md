# Zerion X1 -> PowerX

Zerion X1 keeps all market/trading logic.

It sends only the AI task plus prepared context to PowerX:

```python
client = PowerXClient(
    base_url="https://powerx.example.com",
    api_key=os.environ["POWERX_API_KEY"],
)

result = await client.chat(
    task="deep_reasoning",
    messages=[
        {"role": "system", "content": "Analyze only the supplied context."},
        {"role": "user", "content": prepared_context},
    ],
)
```

PowerX selects the model/runtime. Zerion does not need to know whether the
answer came from 16GB GPU, CPU, mobile fallback, or a future heavy GPU.

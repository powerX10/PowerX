async function safeResponse(r: Response) {
  const text = await r.text();

  let data: any = null;

  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = {
      ok: false,
      error: text || `Backend returned HTTP ${r.status}`,
      status: r.status,
    };
  }

  if (!r.ok) {
    return {
      ok: false,
      status: r.status,
      ...data,
    };
  }

  return data;
}

export async function control(path: string, init: RequestInit = {}) {
  const b = process.env.POWERX_CONTROL_API_URL;
  const t = process.env.POWERX_CONTROL_TOKEN;

  if (!b || !t) {
    return {
      ok: false,
      error: "PowerX control backend is not configured yet.",
    };
  }

  try {
    const r = await fetch(
      b.replace(/\/$/, "") + path,
      {
        ...init,
        headers: {
          ...(init.headers || {}),
          Authorization: `Bearer ${t}`,
        },
        cache: "no-store",
      }
    );

    return await safeResponse(r);
  } catch (e: any) {
    return {
      ok: false,
      error: e?.message || "PowerX control backend request failed.",
    };
  }
}

export async function infer(body: unknown) {
  const b = process.env.POWERX_PRODUCTION_API_URL;
  const k = process.env.POWERX_PRODUCTION_API_KEY;

  if (!b || !k) {
    return {
      ok: false,
      error: "PowerX inference backend is not configured yet.",
    };
  }

  try {
    const r = await fetch(
      b.replace(/\/$/, "") + "/v1/ma",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${k}`,
        },
        body: JSON.stringify(body),
        cache: "no-store",
      }
    );

    return await safeResponse(r);
  } catch (e: any) {
    return {
      ok: false,
      error: e?.message || "PowerX inference backend request failed.",
    };
  }
}

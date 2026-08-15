"use client";

import { useState } from "react";
import {
  GoogleAuthProvider,
  signInWithEmailAndPassword,
  signInWithPopup,
} from "firebase/auth";
import { getFirebaseAuth } from "@/lib/firebase-client";

const OWNER_EMAIL = "syedafsharkhadri63@gmail.com";

export function Login() {
  const [email, setEmail] = useState(OWNER_EMAIL);
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);

  async function createServerSession(user: any) {
    const idToken = await user.getIdToken(true);

    const response = await fetch("/api/auth/bootstrap", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ idToken }),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error || "PowerX login rejected");
    }

    window.location.href = "/dashboard";
  }

  async function emailLogin() {
    try {
      setBusy(true);
      setMsg("");

      if (email.trim().toLowerCase() !== OWNER_EMAIL) {
        throw new Error("This PowerX account is private.");
      }

      const credential = await signInWithEmailAndPassword(
        getFirebaseAuth(),
        email.trim(),
        password
      );

      await createServerSession(credential.user);
    } catch (error: any) {
      setMsg(error?.message || String(error));
    } finally {
      setBusy(false);
    }
  }

  async function googleLogin() {
    try {
      setBusy(true);
      setMsg("");

      const provider = new GoogleAuthProvider();
      provider.setCustomParameters({
        prompt: "select_account",
      });

      const credential = await signInWithPopup(
        getFirebaseAuth(),
        provider
      );

      const userEmail = credential.user.email?.toLowerCase();

      if (userEmail !== OWNER_EMAIL) {
        await getFirebaseAuth().signOut();
        throw new Error("Only the PowerX owner account is allowed.");
      }

      await createServerSession(credential.user);
    } catch (error: any) {
      setMsg(error?.message || String(error));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card login">
      <div className="logo">X</div>

      <h1>PowerX</h1>
      <p className="muted">Private AI control center.</p>

      <div className="stack">
        <input
          className="input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          autoComplete="email"
        />

        <input
          className="input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          autoComplete="current-password"
          onKeyDown={(e) => {
            if (e.key === "Enter") emailLogin();
          }}
        />

        <button
          className="btn primary"
          onClick={emailLogin}
          disabled={busy}
        >
          {busy ? "Signing in..." : "Sign in"}
        </button>

        <button
          className="btn"
          onClick={googleLogin}
          disabled={busy}
        >
          Continue with Google
        </button>

        {msg && <div className="error">{msg}</div>}
      </div>
    </div>
  );
}

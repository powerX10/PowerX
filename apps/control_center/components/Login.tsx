"use client";

import { useState } from "react";
import {
  GoogleAuthProvider,
  signInWithEmailAndPassword,
  signInWithPopup,
} from "firebase/auth";
import { prepareFirebaseAuth } from "@/lib/firebase-client";

const OWNER_EMAIL = "syedafsharkhadri63@gmail.com";

export function Login() {
  const [email, setEmail] = useState(OWNER_EMAIL);
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  async function finishLogin(user: any) {
    const idToken = await user.getIdToken(true);

    const response = await fetch("/api/auth/bootstrap", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({ idToken }),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok || !data.ok) {
      throw new Error(data.error || "PowerX session creation failed");
    }

    window.location.assign("/dashboard");
  }

  async function loginWithEmail() {
    try {
      setBusy(true);
      setMessage("");

      const normalizedEmail = email.trim().toLowerCase();

      if (normalizedEmail !== OWNER_EMAIL) {
        throw new Error("Only the PowerX owner account can sign in.");
      }

      if (!password) {
        throw new Error("Enter your password.");
      }

      const auth = await prepareFirebaseAuth();

      const result = await signInWithEmailAndPassword(
        auth,
        normalizedEmail,
        password
      );

      await finishLogin(result.user);
    } catch (error: any) {
      setMessage(error?.message || "Unable to sign in.");
    } finally {
      setBusy(false);
    }
  }

  async function loginWithGoogle() {
    try {
      setBusy(true);
      setMessage("");

      const auth = await prepareFirebaseAuth();

      const provider = new GoogleAuthProvider();
      provider.setCustomParameters({
        prompt: "select_account",
      });

      const result = await signInWithPopup(auth, provider);

      if (result.user.email?.toLowerCase() !== OWNER_EMAIL) {
        await auth.signOut();
        throw new Error(
          "Only the PowerX owner Google account can sign in."
        );
      }

      await finishLogin(result.user);
    } catch (error: any) {
      setMessage(error?.message || "Google sign in failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="stack" style={{ width: "100%" }}>
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
          if (e.key === "Enter") loginWithEmail();
        }}
      />

      <button
        className="btn primary"
        onClick={loginWithEmail}
        disabled={busy}
      >
        {busy ? "Signing in..." : "Sign in to PowerX"}
      </button>

      <div className="muted">or</div>

      <button
        className="btn"
        onClick={loginWithGoogle}
        disabled={busy}
      >
        Continue with Google
      </button>

      {message && <div className="error">{message}</div>}
    </div>
  );
}

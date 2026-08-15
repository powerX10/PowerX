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
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  async function finishLogin(user: any) {
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
      throw new Error(data.error || "PowerX login failed");
    }

    window.location.href = "/dashboard";
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

      const result = await signInWithEmailAndPassword(
        getFirebaseAuth(),
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

      const provider = new GoogleAuthProvider();

      provider.setCustomParameters({
        prompt: "select_account",
      });

      const result = await signInWithPopup(
        getFirebaseAuth(),
        provider
      );

      const signedEmail =
        result.user.email?.toLowerCase();

      if (signedEmail !== OWNER_EMAIL) {
        await getFirebaseAuth().signOut();
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
      <div style={{ textAlign: "left" }}>
        <label className="muted">Email</label>

        <input
          className="input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
          placeholder="Enter email"
          style={{ marginTop: 7 }}
        />
      </div>

      <div style={{ textAlign: "left" }}>
        <label className="muted">Password</label>

        <input
          className="input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
          placeholder="Enter password"
          style={{ marginTop: 7 }}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              loginWithEmail();
            }
          }}
        />
      </div>

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

      {message && (
        <div className="error">
          {message}
        </div>
      )}
    </div>
  );
}

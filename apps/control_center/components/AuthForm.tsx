"use client";

import { useState } from "react";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  sendPasswordResetEmail,
  updateProfile,
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";
import { prepareFirebaseAuth } from "@/lib/firebase-client";
import { useRouter } from "next/navigation";

export default function AuthForm({
  mode,
}: {
  mode: "login" | "signup" | "reset";
}) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);

  const router = useRouter();

  async function bootstrap(idToken: string) {
    const r = await fetch("/api/auth/bootstrap", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ idToken }),
    });

    if (!r.ok) {
      throw new Error(await r.text());
    }

    router.push("/dashboard");
    router.refresh();
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();

    setBusy(true);
    setMsg("");

    try {
      const auth = await prepareFirebaseAuth();

      if (mode === "reset") {
        await sendPasswordResetEmail(auth, email);
        setMsg("Password reset email sent.");
        return;
      }

      const cred =
        mode === "signup"
          ? await createUserWithEmailAndPassword(auth, email, password)
          : await signInWithEmailAndPassword(auth, email, password);

      if (mode === "signup" && name) {
        await updateProfile(cred.user, {
          displayName: name,
        });
      }

      await bootstrap(await cred.user.getIdToken());
    } catch (err: any) {
      setMsg(err?.message || "Authentication failed");
    } finally {
      setBusy(false);
    }
  }

  async function continueWithGoogle() {
    setBusy(true);
    setMsg("");

    try {
      const auth = await prepareFirebaseAuth();

      const provider = new GoogleAuthProvider();

      provider.setCustomParameters({
        prompt: "select_account",
      });

      const cred = await signInWithPopup(auth, provider);

      await bootstrap(await cred.user.getIdToken());
    } catch (err: any) {
      setMsg(err?.message || "Google Sign-In failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <form onSubmit={submit}>
        {mode === "signup" && (
          <div className="field">
            <label>Name</label>
            <input
              className="input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
        )}

        <div className="field">
          <label>Email</label>
          <input
            className="input"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        {mode !== "reset" && (
          <div className="field">
            <label>Password</label>
            <input
              className="input"
              type="password"
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
        )}

        {msg && (
          <p
            style={{
              color: msg.includes("sent") ? "#79ffa9" : "#ff8590",
              fontSize: 13,
            }}
          >
            {msg}
          </p>
        )}

        <button
          className="btn btnPrimary"
          style={{
            width: "100%",
            marginTop: 8,
          }}
          disabled={busy}
        >
          {busy
            ? "Please wait…"
            : mode === "login"
              ? "Login"
              : mode === "signup"
                ? "Create account"
                : "Send reset link"}
        </button>
      </form>

      {mode !== "reset" && (
        <>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              margin: "18px 0",
              color: "#718096",
              fontSize: 12,
            }}
          >
            <div
              style={{
                height: 1,
                flex: 1,
                background: "#202b3a",
              }}
            />
            OR
            <div
              style={{
                height: 1,
                flex: 1,
                background: "#202b3a",
              }}
            />
          </div>

          <button
            type="button"
            className="btn"
            style={{
              width: "100%",
              background: "#ffffff",
              color: "#111827",
              fontWeight: 800,
            }}
            disabled={busy}
            onClick={continueWithGoogle}
          >
            Continue with Google
          </button>
        </>
      )}
    </div>
  );
}

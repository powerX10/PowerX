import { Login } from "@/components/Login";

export default function HomePage() {
  return (
    <main className="login-wrap">
      <section className="card login">
        <div className="logo">X</div>

        <h1>PowerX</h1>

        <p className="muted">
          Private AI model control center for managing AI runtimes,
          model routing, system health, usage and inference from one place.
        </p>

        <div
          style={{
            width: "100%",
            height: "1px",
            background: "var(--line)",
            margin: "18px 0",
          }}
        />

        <Login />
      </section>
    </main>
  );
}

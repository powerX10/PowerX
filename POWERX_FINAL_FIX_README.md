# PowerX Final Fix
Architecture: browser/UI -> Vercel+Firestore broker -> healthy mobile node first -> CPU node fallback -> optional GPU.
Modal is no longer required for normal UI, routing, API, or chat job dispatch.
A model file has no CPU of its own: true 24x7 CPU inference needs an actual always-on machine running the included CPU node worker.

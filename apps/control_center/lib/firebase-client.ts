import { initializeApp, getApps } from "firebase/app";
import {
  getAuth,
  setPersistence,
  browserSessionPersistence,
} from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCMLDuHX-CoFnV86xSnsWgnJsDgCZlPDis",
  authDomain: "powerx-efc15.firebaseapp.com",
  projectId: "powerx-efc15",
  storageBucket: "powerx-efc15.firebasestorage.app",
  messagingSenderId: "630939648634",
  appId: "1:630939648634:web:608298c44e1fd2d1ce31c3",
  measurementId: "G-0CHJD7329P",
};

export function getFirebaseAuth() {
  const app = getApps()[0] ?? initializeApp(firebaseConfig);
  return getAuth(app);
}

export async function prepareFirebaseAuth() {
  const auth = getFirebaseAuth();

  try {
    await setPersistence(auth, browserSessionPersistence);
  } catch {
    // Ignore browser storage persistence issues.
    // PowerX uses its own secure server session after login.
  }

  return auth;
}

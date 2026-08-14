import { getApps, initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCMLDuHX-CoFnV86xSnsWgnJsDgCZlPDis",
  authDomain: "powerx-efc15.firebaseapp.com",
  projectId: "powerx-efc15",
  storageBucket: "powerx-efc15.firebasestorage.app",
  messagingSenderId: "630939648634",
  appId: "1:630939648634:web:608298c44e1fd2d1ce31c3",
  measurementId: "G-0CHJD7329P"
};

export function getFirebaseAuth() {
  const app = getApps()[0] ?? initializeApp(firebaseConfig);
  return getAuth(app);
}

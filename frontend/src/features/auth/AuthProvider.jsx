import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  getRedirectResult,
  onIdTokenChanged,
  signInWithPopup,
  signInWithRedirect,
  signOut as firebaseSignOut,
} from "firebase/auth";
import api from "../../lib/api";
import { auth, googleProvider, isFirebaseConfigured } from "../../lib/firebase";
import { detectInAppBrowser } from "../../lib/inAppBrowser";
import { AuthContext } from "./AuthContext";
import InAppBrowserNotice from "./InAppBrowserNotice";

const IGNORED_POPUP_ERRORS = new Set([
  "auth/popup-closed-by-user",
  "auth/cancelled-popup-request",
]);

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [backendUser, setBackendUser] = useState(null);
  const [loading, setLoading] = useState(isFirebaseConfigured);
  const [authError, setAuthError] = useState(null);
  const [noticeOpen, setNoticeOpen] = useState(false);
  const syncedUidRef = useRef(null);

  useEffect(() => {
    if (!auth) return undefined;

    getRedirectResult(auth).catch((err) => {
      setAuthError(err?.code || "auth/unknown");
    });

    return onIdTokenChanged(auth, async (firebaseUser) => {
      setUser(firebaseUser);
      if (!firebaseUser) {
        syncedUidRef.current = null;
        setBackendUser(null);
        setLoading(false);
        return;
      }
      // El token se renueva cada hora: solo sincronizamos con el backend al cambiar de usuario.
      if (syncedUidRef.current !== firebaseUser.uid) {
        try {
          const me = await api.json("/api/v1/me");
          syncedUidRef.current = firebaseUser.uid;
          setBackendUser(me);
          setAuthError(null);
        } catch (err) {
          setBackendUser(null);
          setAuthError(err?.message || "No se pudo conectar con el servidor.");
        }
      }
      setLoading(false);
    });
  }, []);

  const signInWithGoogle = useCallback(async () => {
    if (!auth) return;
    if (detectInAppBrowser()) {
      setNoticeOpen(true);
      return;
    }
    setAuthError(null);
    try {
      await signInWithPopup(auth, googleProvider);
    } catch (err) {
      if (err?.code === "auth/popup-blocked") {
        await signInWithRedirect(auth, googleProvider);
      } else if (!IGNORED_POPUP_ERRORS.has(err?.code)) {
        setAuthError(err?.code || "auth/unknown");
      }
    }
  }, []);

  const signOut = useCallback(async () => {
    if (!auth) return;
    await firebaseSignOut(auth);
  }, []);

  const value = useMemo(
    () => ({
      user,
      backendUser,
      loading,
      enabled: isFirebaseConfigured,
      authError,
      signInWithGoogle,
      signOut,
    }),
    [user, backendUser, loading, authError, signInWithGoogle, signOut]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
      <InAppBrowserNotice
        open={noticeOpen}
        appName={detectInAppBrowser()}
        onClose={() => setNoticeOpen(false)}
      />
    </AuthContext.Provider>
  );
}

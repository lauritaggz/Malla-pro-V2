import { signOut as firebaseSignOut } from "firebase/auth";
import { auth } from "./firebase";

const DEFAULT_API_URL = "http://localhost:8000";

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Cliente HTTP con el ID token de Firebase.
 * Ante un 401 refresca el token (getIdToken(true)) y reintenta una sola vez;
 * si vuelve a dar 401 llama a onUnauthorized (cerrar sesión).
 */
export function createApi({
  getUser,
  onUnauthorized,
  baseUrl = DEFAULT_API_URL,
  fetchFn = (...args) => globalThis.fetch(...args),
}) {
  const root = baseUrl.replace(/\/$/, "");

  async function fetchWithAuth(path, options = {}) {
    const user = getUser();

    const send = async (forceRefresh) => {
      const headers = new Headers(options.headers);
      if (user) {
        headers.set("Authorization", `Bearer ${await user.getIdToken(forceRefresh)}`);
      }
      return fetchFn(`${root}${path}`, { ...options, headers });
    };

    let response = await send(false);
    if (response.status === 401 && user) {
      response = await send(true);
      if (response.status === 401) {
        await onUnauthorized?.();
      }
    }
    return response;
  }

  async function json(path, options) {
    const response = await fetchWithAuth(path, options);
    if (!response.ok) {
      let detail = `Error ${response.status}`;
      try {
        const body = await response.json();
        if (typeof body?.detail === "string") detail = body.detail;
      } catch {
        /* cuerpo no JSON */
      }
      throw new ApiError(response.status, detail);
    }
    return response.json();
  }

  return { fetch: fetchWithAuth, json };
}

const api = createApi({
  getUser: () => auth?.currentUser ?? null,
  onUnauthorized: () => (auth ? firebaseSignOut(auth) : undefined),
  baseUrl: import.meta.env.VITE_API_URL || DEFAULT_API_URL,
});

export default api;

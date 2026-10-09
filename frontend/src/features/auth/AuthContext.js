import { createContext } from "react";

export const AuthContext = createContext({
  user: null,
  backendUser: null,
  loading: false,
  enabled: false,
  authError: null,
  signInWithGoogle: async () => {},
  signOut: async () => {},
});

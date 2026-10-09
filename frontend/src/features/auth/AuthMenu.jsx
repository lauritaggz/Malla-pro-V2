import { useEffect, useRef, useState } from "react";
import { LogIn, LogOut } from "lucide-react";
import { useAuth } from "./useAuth";

export function UserAvatar({ user, backendUser, className = "w-8.5 h-8.5" }) {
  const photo = backendUser?.photo_url || user?.photoURL;
  const name = backendUser?.display_name || user?.displayName || user?.email || "?";
  if (photo) {
    return (
      <img
        src={photo}
        alt=""
        referrerPolicy="no-referrer"
        className={`${className} rounded-full object-cover`}
      />
    );
  }
  return (
    <span
      className={`${className} rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold`}
    >
      {name.trim().charAt(0).toUpperCase()}
    </span>
  );
}

/** Botón de sesión para la Navbar de escritorio (en móvil se usa la barra inferior). */
export default function AuthMenu() {
  const { enabled, loading, user, backendUser, signInWithGoogle, signOut } = useAuth();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  if (!enabled || loading) return null;

  if (!user) {
    return (
      <button
        type="button"
        onClick={signInWithGoogle}
        className="hidden sm:inline-flex h-8.5 items-center gap-1.5 rounded-full border border-borderColor px-3 text-xs font-semibold text-textPrimary hover:bg-borderColor/20 transition-colors"
      >
        <LogIn className="w-3.5 h-3.5" aria-hidden />
        Entrar con Google
      </button>
    );
  }

  return (
    <div ref={ref} className="relative hidden sm:block">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-label="Menú de cuenta"
        aria-expanded={open}
        className="rounded-full border border-borderColor"
      >
        <UserAvatar user={user} backendUser={backendUser} />
      </button>
      {open && (
        <div className="absolute right-0 top-full mt-2 w-60 rounded-2xl border border-borderColor bg-bgSecondary p-3 shadow-xl z-50">
          <p className="truncate text-xs font-bold text-textPrimary">
            {backendUser?.display_name || user.displayName}
          </p>
          <p className="truncate text-[11px] text-textSecondary">
            {backendUser?.email || user.email}
          </p>
          <button
            type="button"
            onClick={() => {
              setOpen(false);
              signOut();
            }}
            className="mt-2.5 flex w-full items-center gap-2 rounded-xl px-2.5 py-1.5 text-xs font-semibold text-textPrimary hover:bg-bgPrimary/60"
          >
            <LogOut className="w-3.5 h-3.5 text-textSecondary" aria-hidden />
            Cerrar sesión
          </button>
        </div>
      )}
    </div>
  );
}

import { useEffect, useRef, useState } from "react";
import { LogIn, LogOut } from "lucide-react";
import { useAuth } from "./useAuth";

/** Avatar redondo de tamaño fijo (por defecto 32 px); cae a la inicial si la foto falla. */
export function UserAvatar({ user, backendUser, className = "w-8 h-8" }) {
  const photo = backendUser?.photo_url || user?.photoURL;
  const name = backendUser?.display_name || user?.displayName || user?.email || "?";
  const [failedPhoto, setFailedPhoto] = useState(null);
  const base = `${className} shrink-0 rounded-full`;

  if (photo && failedPhoto !== photo) {
    return (
      <img
        src={photo}
        alt=""
        referrerPolicy="no-referrer"
        onError={() => setFailedPhoto(photo)}
        className={`${base} object-cover`}
      />
    );
  }
  return (
    <span
      aria-hidden
      className={`${base} bg-primary text-white flex items-center justify-center text-xs font-bold leading-none select-none`}
    >
      {name.trim().charAt(0).toUpperCase()}
    </span>
  );
}

/**
 * Sesión en el riel lateral de escritorio (la barra superior y la inferior son solo móvil).
 * Mismo aspecto que los botones del riel: icono arriba y etiqueta abajo.
 */
export function RailAccountButton() {
  const { enabled, loading, user, backendUser, signInWithGoogle, signOut } = useAuth();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    const onKey = (e) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("pointerdown", handler);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", handler);
      document.removeEventListener("keydown", onKey);
    };
  }, []);

  if (!enabled || loading) return null;

  const railBtn =
    "relative w-[60px] flex flex-col items-center gap-1 rounded-xl py-2 text-[12px] font-semibold leading-none transition-[background-color,color] duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 text-textSecondary hover:text-textPrimary hover:bg-borderColor/40";

  if (!user) {
    return (
      <button type="button" onClick={signInWithGoogle} className={railBtn} title="Entrar con Google">
        <LogIn className="w-5 h-5" aria-hidden />
        <span>Entrar</span>
      </button>
    );
  }

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        aria-label="Menú de cuenta"
        aria-expanded={open}
        className={railBtn}
      >
        <UserAvatar user={user} backendUser={backendUser} className="w-6 h-6" />
        <span>Cuenta</span>
      </button>
      {open && (
        <div className="absolute left-full bottom-0 ml-3 w-60 rounded-2xl border border-borderColor bg-bgSecondary p-3 shadow-xl z-50">
          <p className="truncate text-xs font-bold text-textPrimary">
            {backendUser?.display_name || user.displayName}
          </p>
          <p className="truncate text-[12px] text-textSecondary">
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

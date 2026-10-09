import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BookMarked, CalendarDays, CalendarRange, LogIn, LogOut, MessageCircle } from "lucide-react";
import { useAuth } from "../features/auth/useAuth";
import { UserAvatar } from "../features/auth/AuthMenu";

export default function MobileBottomNav({
  vistaPrincipal = "malla",
  setVistaPrincipal,
  onGuardLeave,
}) {
  const navigate = useNavigate();
  const { enabled, loading, user, backendUser, signInWithGoogle, signOut } = useAuth();
  const [accountOpen, setAccountOpen] = useState(false);
  const showAuth = enabled && !loading;

  const navItems = [
    {
      label: "Mi malla",
      value: "malla",
      icon: <BookMarked className="w-5.5 h-5.5" />,
      onClick: () => {
        setVistaPrincipal("malla");
        navigate("/app");
      }
    },
    {
      label: "Periodo actual",
      value: "periodo-actual",
      icon: <CalendarDays className="w-5.5 h-5.5" />,
      onClick: () => {
        if (onGuardLeave && !onGuardLeave()) return;
        setVistaPrincipal("periodo-actual");
        navigate("/app");
      }
    },
    {
      label: "Horario",
      value: "toma-de-ramos",
      icon: <CalendarRange className="w-5.5 h-5.5" />,
      onClick: () => {
        if (onGuardLeave && !onGuardLeave()) return;
        setVistaPrincipal("toma-de-ramos");
        navigate("/programacion-academica");
      }
    },
    {
      label: "Tutorías",
      value: "tutorias",
      icon: <MessageCircle className="w-5.5 h-5.5" />,
      onClick: () => {
        if (onGuardLeave && !onGuardLeave()) return;
        setVistaPrincipal("tutorias");
        navigate("/app");
      }
    }
  ];

  return (
    <div className={`fixed bottom-0 left-0 right-0 h-[calc(4rem+env(safe-area-inset-bottom,0px))] bg-bgSecondary/90 backdrop-blur-xl border-t border-borderColor/50 z-[90] sm:hidden grid ${showAuth ? "grid-cols-5" : "grid-cols-4"} items-center px-1 pb-[env(safe-area-inset-bottom,0px)] shadow-[0_-2px_12px_rgba(0,0,0,0.06)]`}>
      {navItems.map((item) => {
        const isActive = vistaPrincipal === item.value;
        return (
          <button
            key={item.value}
            onClick={item.onClick}
            className={`flex flex-col items-center justify-center p-1 transition-all duration-200 gap-1
              ${isActive ? "text-primary font-bold scale-105" : "text-textSecondary"}`}
          >
            <div className={`transition-transform duration-200 ${isActive ? "scale-105 text-primary" : "text-textSecondary/80"}`}>
              {item.icon}
            </div>
            <span className="text-[9.5px] font-semibold leading-none truncate w-full text-center">
              {item.label}
            </span>
          </button>
        );
      })}
      {showAuth && (
        <div className="relative flex items-center justify-center">
          <button
            type="button"
            onClick={() => (user ? setAccountOpen((v) => !v) : signInWithGoogle())}
            aria-label={user ? "Menú de cuenta" : "Entrar con Google"}
            className="flex flex-col items-center justify-center p-1 gap-1 text-textSecondary"
          >
            {user ? (
              <UserAvatar user={user} backendUser={backendUser} className="w-6 h-6" />
            ) : (
              <LogIn className="w-5.5 h-5.5" />
            )}
            <span className="text-[9.5px] font-semibold leading-none">
              {user ? "Cuenta" : "Entrar"}
            </span>
          </button>
          {user && accountOpen && (
            <div className="absolute bottom-full right-1 mb-2 w-56 rounded-2xl border border-borderColor bg-bgSecondary p-3 shadow-xl">
              <p className="truncate text-xs font-bold text-textPrimary">
                {backendUser?.display_name || user.displayName}
              </p>
              <p className="truncate text-[11px] text-textSecondary">
                {backendUser?.email || user.email}
              </p>
              <button
                type="button"
                onClick={() => {
                  setAccountOpen(false);
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
      )}
    </div>
  );
}

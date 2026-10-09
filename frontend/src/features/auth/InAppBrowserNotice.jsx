import { useRef, useState } from "react";
import { Check, Copy, X } from "lucide-react";

export default function InAppBrowserNotice({ open, appName, onClose }) {
  const [copied, setCopied] = useState(false);
  const inputRef = useRef(null);

  if (!open) return null;

  const link = typeof window !== "undefined" ? window.location.href : "";

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(link);
    } catch {
      inputRef.current?.select();
      document.execCommand?.("copy");
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="in-app-browser-title"
    >
      <div className="relative w-full max-w-sm rounded-2xl border border-borderColor bg-bgSecondary p-5 shadow-xl">
        <button
          type="button"
          onClick={onClose}
          aria-label="Cerrar aviso"
          className="absolute right-3 top-3 text-textSecondary hover:text-textPrimary"
        >
          <X className="h-4 w-4" />
        </button>
        <h2 id="in-app-browser-title" className="text-sm font-bold text-textPrimary">
          Para iniciar sesión, abre MallaPro en Chrome o Safari
        </h2>
        <p className="mt-2 text-xs text-textSecondary">
          {appName ? `El navegador de ${appName}` : "Este navegador"} no permite iniciar sesión con
          Google. Copia el enlace y ábrelo en tu navegador.
        </p>
        <input
          ref={inputRef}
          readOnly
          value={link}
          className="mt-3 w-full rounded-lg border border-borderColor bg-bgPrimary px-2.5 py-2 text-xs text-textPrimary"
        />
        <button
          type="button"
          onClick={handleCopy}
          className="mt-3 flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-3 py-2 text-xs font-bold text-white"
        >
          {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
          {copied ? "Enlace copiado" : "Copiar enlace"}
        </button>
      </div>
    </div>
  );
}

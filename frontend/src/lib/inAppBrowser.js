// Los navegadores internos (Instagram, Facebook, TikTok…) bloquean el login de Google.
const IN_APP_PATTERNS = [
  [/Instagram/i, "Instagram"],
  [/FBAN|FBAV|FB_IAB/i, "Facebook"],
  [/musical_ly|BytedanceWebview|TikTok/i, "TikTok"],
  [/\bLine\//i, "Line"],
  [/Snapchat/i, "Snapchat"],
];

/** Devuelve el nombre de la app si el userAgent es un navegador interno; si no, null. */
export function detectInAppBrowser(userAgent) {
  const ua = userAgent ?? (typeof navigator !== "undefined" ? navigator.userAgent : "");
  for (const [pattern, name] of IN_APP_PATTERNS) {
    if (pattern.test(ua)) return name;
  }
  return null;
}

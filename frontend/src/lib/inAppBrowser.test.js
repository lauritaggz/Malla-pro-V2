import { describe, expect, it } from "vitest";
import { detectInAppBrowser } from "./inAppBrowser.js";

const UAS = {
  instagram:
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/21A329 Instagram 300.0.0.0",
  facebook:
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/450.0]",
  facebookIos: "Mozilla/5.0 (iPhone) Mobile/21A329 [FBAN/FBIOS;FBAV/450.0;FBBV/1]",
  tiktok: "Mozilla/5.0 (Linux; Android 12) Chrome/110 Mobile Safari/537.36 musical_ly_30.0.0",
  tiktokBytedance: "Mozilla/5.0 (iPhone) Mobile/15E148 BytedanceWebview/d8a21c6",
  line: "Mozilla/5.0 (iPhone) Mobile/15E148 Safari Line/13.0.0",
  snapchat: "Mozilla/5.0 (iPhone) Mobile/15E148 Snapchat/12.0.0.0",
  chrome:
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
  safari:
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
};

describe("detectInAppBrowser", () => {
  it("detects in-app browsers", () => {
    expect(detectInAppBrowser(UAS.instagram)).toBe("Instagram");
    expect(detectInAppBrowser(UAS.facebook)).toBe("Facebook");
    expect(detectInAppBrowser(UAS.facebookIos)).toBe("Facebook");
    expect(detectInAppBrowser(UAS.tiktok)).toBe("TikTok");
    expect(detectInAppBrowser(UAS.tiktokBytedance)).toBe("TikTok");
    expect(detectInAppBrowser(UAS.line)).toBe("Line");
    expect(detectInAppBrowser(UAS.snapchat)).toBe("Snapchat");
  });

  it("returns null for regular browsers", () => {
    expect(detectInAppBrowser(UAS.chrome)).toBeNull();
    expect(detectInAppBrowser(UAS.safari)).toBeNull();
    expect(detectInAppBrowser("")).toBeNull();
  });
});

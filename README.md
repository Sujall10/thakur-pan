# Thakur Pan — v3 (4 themes + motion)
Open index.html in a browser. Use the **Theme** button in the top bar to switch designs live
(Night Market · Paan Pop · Royal Mughal · Fresh Mint). Add ?theme=pop to a URL to force one.

To ship ONE theme: in build.py set DEFAULT_THEME = "royal" (etc.) and LOCK_THEME = True, run `python3 build.py`.
This removes the switcher and loads only that theme's fonts.
Edit phone/links at the top of build.py. All copy and images are unchanged from v2.
Fonts load from Google Fonts (needs internet).

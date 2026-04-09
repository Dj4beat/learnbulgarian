"""
fix_bulgarian_fonts.py
Run this script in your  C:\\Users\\Dj4be\\Desktop\\New Bulgarian  folder.
It patches every .html file to fix the handwriting/cursive Cyrillic font issue.

Usage:
  1. Copy this file into your New Bulgarian folder
  2. Double-click it (or run:  python fix_bulgarian_fonts.py  in a terminal)
  3. Upload all the patched .html files to your server
"""

import os
import re

# ── What we're fixing ────────────────────────────────────────────────────────
# Google Fonts serves Russian Cyrillic glyph shapes by default.
# Bulgarian uses different printed forms for г д п т.
# Without the fix, those letters look like handwriting on any device
# that doesn't have the Bulgarian language pack installed.

OLD_FONT_URL = (
    'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900'
    '&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap'
)
NEW_FONT_URL = (
    'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900'
    '&family=Source+Sans+3:ital,ital,wght@0,400;0,500;0,600;0,700;1,400;1,600'
    '&subset=cyrillic&display=swap'
)

CSS_FIX = (
    '\n/* Bulgarian glyph variant fix */\n'
    '[lang="bg"],.bg-text,.reading-bg,.alpha-cyrillic,'
    '.alpha-example span,td[lang="bg"],p[lang="bg"]{\n'
    '  font-language-override:"BGR";\n'
    '  font-feature-settings:"locl" 1;\n'
    '  text-rendering:optimizeLegibility;\n'
    '}\n'
)

# ── Run ──────────────────────────────────────────────────────────────────────
folder = os.path.dirname(os.path.abspath(__file__))
html_files = [f for f in os.listdir(folder) if f.endswith('.html')]

if not html_files:
    print('No .html files found in this folder.')
    input('Press Enter to close.')
    raise SystemExit

fixed = 0
skipped = 0

for fname in sorted(html_files):
    path = os.path.join(folder, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Update Google Fonts URL
    if OLD_FONT_URL in content:
        content = content.replace(OLD_FONT_URL, NEW_FONT_URL)
        changed = True

    # 2. Inject CSS fix (only if not already present)
    if 'font-language-override' not in content and '</style>' in content:
        content = content.replace('</style>', CSS_FIX + '</style>', 1)
        changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  FIXED   {fname}')
        fixed += 1
    else:
        print(f'  skipped {fname}  (already patched or different font URL)')
        skipped += 1

print()
print(f'Done.  {fixed} file(s) fixed,  {skipped} already up to date.')
print()
input('Press Enter to close.')

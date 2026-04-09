"""
fix_bulgarian_fonts.py  —  v3  (self-hosted font injection)
============================================================
Run this in your  C:\\Users\\Dj4be\\Desktop\\New Bulgarian  folder.

This injects the self-hosted Noto Sans Cyrillic font directly into every
HTML file, bypassing Apple's system font interception entirely.

Usage:
  1. Drop this file into your New Bulgarian folder
  2. Double-click it (or run: python fix_bulgarian_fonts.py in a terminal)
  3. Upload all the patched .html files to your server via FTP
"""

import os
import re

FOLDER = os.path.dirname(os.path.abspath(__file__))

FONT_TAG = (
    '\n<style>\n'
    '/* Self-hosted Noto Sans Cyrillic — bypasses Apple system font substitution */\n'
    '@font-face {\n'
    '  font-family: "Source Sans 3";\n'
    '  font-style: normal;\n'
    '  font-weight: 400 700;\n'
    '  src: url("https://whatchan.co.uk/bulgarian/fonts/noto-sans-cyrillic.woff2") format("woff2");\n'
    '  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;\n'
    '  font-display: swap;\n'
    '}\n'
    '@font-face {\n'
    '  font-family: "Source Sans 3";\n'
    '  font-style: italic;\n'
    '  font-weight: 400;\n'
    '  src: url("https://whatchan.co.uk/bulgarian/fonts/noto-sans-cyrillic-italic.woff2") format("woff2");\n'
    '  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;\n'
    '  font-display: swap;\n'
    '}\n'
    '</style>\n'
)

html_files = sorted([f for f in os.listdir(FOLDER) if f.endswith('.html')])

if not html_files:
    print('No .html files found in this folder.')
    input('Press Enter to close.')
    raise SystemExit

fixed = 0
skipped = 0

for fname in html_files:
    path = os.path.join(FOLDER, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'noto-sans-cyrillic.woff2' in content:
        print('  skipped ' + fname + '  (already patched)')
        skipped += 1
        continue

    # Remove any leftover failed CSS fix attempts
    content = re.sub(
        r'\n?/\* Bulgarian glyph variant fix \*/[^}]*\{[^}]*\}\n?',
        '',
        content
    )

    if '</head>' in content:
        content = content.replace('</head>', FONT_TAG + '</head>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('  FIXED   ' + fname)
        fixed += 1
    else:
        print('  WARNING ' + fname + '  (no </head> tag found — skipped)')
        skipped += 1

print('')
print('Done.  ' + str(fixed) + ' file(s) fixed,  ' + str(skipped) + ' skipped.')
print('')
input('Press Enter to close.')

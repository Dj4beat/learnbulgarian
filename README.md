# bg60day.com

Static 60-day Bulgarian course. `tools/deploy_site.py` uploads an explicit allowlist of public files to IONOS over SFTP. The command is a dry run until you pass `--send`.

## IndexNow

The public IndexNow key is `0d481dd68a148caab456dd159e978704.txt` at the site root. The file contains the key and nothing else. `public_files()` in `tools/deploy_site.py` appends that key file to the allowlist, so the next deploy uploads it.

`tools/indexnow.py` reads the key and, by default, the URLs in `sitemap.xml`. It does not contact IndexNow unless you pass `--send`. Optional positional paths replace the sitemap. HTTP 200 and 202 are success. HTTP 403 and 422 print a warning (the key file may not be live yet) and do not fail a deploy.

```bash
python tools/indexnow.py
python tools/indexnow.py --send
python tools/indexnow.py --send day01.html index.html

python tools/deploy_site.py
python tools/deploy_site.py --send
python tools/deploy_site.py --send --skip-indexnow
```

A real deploy submits the files that were uploaded. If that set cannot be determined, it submits `sitemap.xml` instead. IndexNow problems only print a warning.

`sitemap.xml` still lists `whatchan.co.uk` URLs. A sitemap submission sends those locations as written, so IndexNow may answer 422 until the sitemap uses `bg60day.com`. Deploy submissions use `https://bg60day.com/<path>` for the files that changed.

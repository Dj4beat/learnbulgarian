# Platforms

## IONOS

bg60day.com is a static site. `tools/deploy_site.py` uploads only the allowlist in `PUBLIC_FILES` (course HTML, `sitemap.xml`, the two root font files, and `audio/`) plus the IndexNow key file. Nothing else is added to that set. The Whatchan `.htaccess` is not in the allowlist; it redirects visitors to whatchan.co.uk.

The command is a dry run until `--send`. A real upload needs `paramiko` (`pip install paramiko`) and these environment variables, which the script does not print:

- `IONOS_SFTP_HOST`
- `IONOS_SFTP_USER`
- `IONOS_SFTP_REMOTE_DIR`
- `IONOS_SFTP_PASSWORD` or `IONOS_SFTP_KEY`
- `IONOS_SFTP_PORT` (optional, default 22)

```bash
python tools/deploy_site.py
python tools/deploy_site.py --send
python tools/deploy_site.py --send --skip-indexnow
```

## IndexNow

IndexNow tells participating search engines about new or updated URLs.

- Key file: `0d481dd68a148caab456dd159e978704.txt` at the site root (public by design; included in the deploy allowlist)
- Endpoint: `https://api.indexnow.org/indexnow`
- Payload: `host` `bg60day.com`, `key`, `keyLocation` `https://bg60day.com/0d481dd68a148caab456dd159e978704.txt`, and `urlList`
- URL source: `sitemap.xml`, or the paths passed to `tools/indexnow.py`. After a real deploy, the list is the files uploaded in that run, or the full sitemap when the changed set is unknown.

```bash
python tools/indexnow.py
python tools/indexnow.py --send
python tools/indexnow.py --send day01.html
```

HTTP 200 and 202 mean the batch was accepted. HTTP 403 and 422 print a warning and do not fail the deploy.

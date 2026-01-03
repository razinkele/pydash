import json
import pathlib
from collections import defaultdict

p = pathlib.Path("analysis_artifacts_run_20683602775")
if not p.exists():
    p = pathlib.Path("analysis_artifacts")
hosts = defaultdict(lambda: defaultdict(int))
for har in p.rglob("*.har"):
    try:
        data = json.loads(har.read_text(encoding="utf-8"))
    except Exception as e:
        print("skipping", har, "err", e)
        continue
    entries = data.get("log", {}).get("entries", [])
    for e in entries:
        req = e.get("request", {})
        url = req.get("url", "")
        if not url:
            continue
        host = url.split("/")[2] if "//" in url else ""
        failure = e.get("response", {}).get("_failureText") or str(
            e.get("response", {}).get("status", "")
        )
        if failure and failure not in ("200", "0", ""):
            hosts[host][failure] += 1
# print summary
for host, failures in sorted(hosts.items()):
    print(f"{host}")
    for f, t in failures.items():
        print(f"  {f}: {t}")
print("\nTotal hosts:", len(hosts))

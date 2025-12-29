"""Debug exact garminconnect v0.2.36 API."""
from garminconnect import Garmin

client = Garmin("test", "test")

print("1. Available login methods:")
for m in dir(client):
    if any(x in m.lower() for x in ['login', 'resume', 'oauth', 'mfa', 'verify']):
        print(f"  - {m}")

print("\n2. Garmin.ActivityDownloadFormat:")
try:
    print(f"  FIT = {getattr(Garmin, 'ActivityDownloadFormat', 'Not found')}")
except Exception:
    print("  ActivityDownloadFormat not available")

print("\n3. Test login without credentials:")
try:
    client.login()
    print("  login() works without args")
except Exception as e:
    print(f"  login() error: {e}")

print("\n4. Test resume_login:")
try:
    client.resume_login()
    print("  resume_login() works without args")
except Exception as e:
    print(f"  resume_login() error: {e}")

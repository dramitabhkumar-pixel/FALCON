from kiteconnect import KiteConnect
from config.settings import API_KEY, API_SECRET

kite = KiteConnect(api_key=API_KEY)

request_token = input("Enter Request Token: ").strip()

try:
    data = kite.generate_session(
        request_token=request_token,
        api_secret=API_SECRET
    )

    access_token = data["access_token"]

    print("\n===================================")
    print("ACCESS TOKEN GENERATED SUCCESSFULLY")
    print("===================================")
    print(access_token)

    with open("access_token.txt", "w") as f:
        f.write(access_token)

    print("\nAccess token saved to access_token.txt")

except Exception as e:
    print("\nERROR:")
    print(e)
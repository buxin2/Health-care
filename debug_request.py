from app import app

if __name__ == "__main__":
    with app.test_client() as client:
        resp = client.get("/")
        print("Status:", resp.status_code)
        content = resp.data.decode("utf-8", errors="ignore")
        print("Length:", len(content))
        with open("debug_output.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Wrote debug_output.html")



from init import init_app

a = init_app()

if __name__ == "__main__":
    a.run(host="0.0.0.0", port=8080)

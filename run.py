from __init__ import create_app

portfolio_app = create_app()

if __name__ == "__main__":
    portfolio_app.run(host="0.0.0.0", port=5000)

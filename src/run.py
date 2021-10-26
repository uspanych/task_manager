import uvicorn
import os
import django


def main():
    uvicorn.run(
        'app.app:app',
        host='127.0.0.1',
        port=8080,
        reload=True,
    )


if __name__ == '__main__':
    main()

# Simply CRUD backend

It's used to store screenshots in github pull requests

## Usage

http://127.0.0.1:5000

### POST

`curl -i -F "file=@/Path/to/your/file" http://127.0.0.1:5000/`

### GET

`http://127.0.0.1:5000/uploads/<filenam>`
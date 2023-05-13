# Portfolio API

## Overview
A simply and tailored headless CMS, that allows you to populate your personal/career information. The headless CMS provides an API and API key (after generating and saving it) that will grant you access to your provided information in JSON.

Decoupled from the front-end, with the API, you can make your custom portfolio/resume anyway you want.

https://portfolio-api.com

Here's my personal online porfolio using portfolio-api: <a href="https://tonypham.dev" rel="noopener noreferrer" target="_blank">tonypham.dev</a>

*Please do not provide any sensitive information as this is a personal project with very little security emphasis.

## Usage
You can make an account or you can test it out with the dummy credentials provided on the software.

- Clone the project
- make virtual env for the cloned project and activate the virtual env.
```angular2html
python -m venv env
source env/bin/activate
```
- .env file setup. Make a new file ".env" and copy values from "env_config"
- install required packages
```angular2html
pip install -r requirements.txt
```

#### *Disclaimer

- when running "pip install -r requirements.txt", an error may occur trying to install "psycopg2-binary". If that happens, comment the package from requirements.txt and install it as a standalone.
```angular2html
pip install psycopg2-binary
```
and then run again:
```angular2html
pip install -r requirements.txt
```

## Contribution
1. Open a new issue to start a discussion around your feature or if a bug is discovered.

2. Fork the repository and make your changes. (I'll setup an author.md if there are ever any contributors)

3. Send a pull request.

## License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

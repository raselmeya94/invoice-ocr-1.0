# Project Deployment (Invoice OCR)

## Prerequisites

### Python 3.10 or Above:
This guide assumes you have Python 3.10 or a later version installed. If not, refer to the official documentation for your operating system (OS) on how to install Python. Package manager commands like `sudo apt` (Ubuntu), `curl` (generic), or `brew` (macOS) might be used.

### Package Manager (Pip):
Verify that `pip` (the default package manager for Python) is installed. If it is not installed, you can find installation instructions online for your specific OS.


## Creating a Project Directory and Virtual Environment


### Create a Project Directory:

1. Open your terminal or command prompt.
2. Use the `mkdir` command to create a directory for your project. For example:

```bash
mkdir my_django_project
``` 
3. Navigate into the project directory:

```bash
cd my_django_project
 ```   

### Clone Git repository:

```bash
git clone https://github.com/raselmeya94/invoice-ocr-1.0
```




### Create a Virtual Environment:

1. Use the `python -m venv` command to create a virtual environment named `Invoice_environment` (replace with your desired name):

```bash
python -m venv Invoice_environment
```
  
### Directory Structure:
```bash
my_django_project /(parent_directory)
├─invoice-ocr-1.0/ (git repo)
│  ├──invoice_project/  (Django project directory)
│  │   ├── invoice_app/  (Django app)
│  │   ├── invoice_project/  (project directory)
│  │   ├── db.sqlite3  (SQLite database)
│  │   └── manage.py  (Django management script)
│  └──README.md (Deployment documentation)
└────Invoice_environment
```
### Activating the Virtual Environment:

#### macOS/Linux:
Inside the project directory where located `Invoice_environment` and run the following command
    
```bash
source Invoice_environment/bin/activate
  ``` 

Your terminal prompt will change to indicate that you're working within the virtual environment.



### Dependencies Installation:
Change directory and go to `invoice-ocr-1.0/invoice_project` and run `pip install -r requirements.txt` for installation dependencies.
```bash
cd invoice-ocr-1.0/invoice_project
```
Then run the following command
```bash
pip install -r requirements.txt
```
### Export API Key

Export `API KEY` inside this environment following this command:
```bash
export GEMINI_API_KEY="Your_API_KEY"
```
### Run Invoice OCR application:

Then run the following command
```bash
python manage.py runserver 0.0.0.0:8000 <<your available port>>
```

The server will typically listen on the default port 8000. You can access your application by opening http://localhost:8000/ in your web browser.



# xmarie

## Introduction
**xmarie** is a web application allowing you to run, execute and profile code written for the XMARIE architecture.

## Whole project
The web app is composed of four components. 
- Web server (this repository)
- Front end (https://github.com/eryktr/xmarie-frontend)
- **xmarie-vm** library (https://github.com/eryktr/xmarie-vm)
- Automated testing system (https://github.com/eryktr/xmarie-ts)

## Architecture overview
A detailed **XMARIE** architecture overview can be found in the [xmarie-vm](https://github.com/eryktr/xmarie-vm) repository.

## App overview
![outlook](https://user-images.githubusercontent.com/36778031/108757681-71ab1800-754a-11eb-8787-b90c3aab53a0.png)

### Running
![run](https://user-images.githubusercontent.com/36778031/108757654-69eb7380-754a-11eb-8976-c4ac9d443191.png)

### Debugging
![debug](https://user-images.githubusercontent.com/36778031/108757664-6d7efa80-754a-11eb-9ded-29d65d78d45c.png)
![step](https://user-images.githubusercontent.com/36778031/108757687-7374db80-754a-11eb-8b7c-253f0562d1e9.png)

### Profiling
![profile](https://user-images.githubusercontent.com/36778031/108757656-6bb53700-754a-11eb-8816-5d5bbeca6c4f.png)

## Running the whole app
1. Clone this repository
2. In the main directory, run 
```
pip install -r requirements.txt
```
3. Start the web server
```
python3 -m flask run
```
5. Clone the **xmarie-frontend** repository
6. Open the **index.html** file in your browser.

# CarScrapper
The CarScrapper project aims to create a Java GUI to download ads from some
websites like [coches](https://www.coches.net/), 
[milanuncios](https://www.milanuncios.com/) and 
[autoscout24](https://www.autoscout24.es/) to a '.csv' file.

## The GUI
The GUI of the program is made with Java and NETBeans. It consists of various
dropdowns, a download and a config button. With the dropdows you can specify
what you want to download specifically and from which website. With the config
button you can choose where the file will be downloaded.

## Setting it up
### Windows
The idea of this GUI is for it to be available to anyone with java installed in
their devices and nothing else. To achieve this we use pyinstaller to compile
the python modules into a single executable (using a virtual environment) to 
achieve less memory usage, Launch4J, to create the Java executable, and Inno 
setup, to create an installer.

Launch4J and Inno setup must be configured manually, but you can automate
creating a virtual-env with python and an executable with the following code:
```
pip
```


plateGuard
==========
## Purpose
To be able to protect personal information in mass video data collection

## Proof of Concept:
License plate encryption in mass collection of videos through security cameras, traffic cameras and autonomous vehicles.

### Installation
#### Requirements
- Python 3.6.5
- OpenALPR

#### Linux
- Python 3.6.5
  ```
  sudo apt-get update
  sudo apt-get install python3.6
  ```
- OpenALPR
  Installation steps taken from OpenALPR documentation found: https://github.com/openalpr/openalpr/wiki/Compilation-instructions-(Ubuntu-Linux)
  Followed Ubuntu 14.04+ steps for installation as follows:
  ```
  # Install Prerequisites
  sudo apt-get install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
  sudo apt-get install liblog4cplus-dev libcurl3-dev

  # If using the daemon, install beanstalkd
  sudo apt-get install beanstalkd

  # Clone the latest code from GitHub
  git clone https://github.com/openalpr/openalpr.git

  # Setup the build directory
  cd openalpr/src
  mkdir build
  cd build

  # setup the compile environment
  cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..

  # compile the library
  make

  # Install the binaries/libraries to your local system (prefix is /usr)
  sudo make install
  ```

- Set up Python Bindings
  ```
  cd openalpr/src/bindings/python/
  sudo python3 setup.py install
  ```

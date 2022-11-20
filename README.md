# ![](pyhb/typing_tester/assets/pyhb_icon.png) pyhb
  ![](https://img.shields.io/github/license/blankRiot96/pyhb) 
  ![](https://img.shields.io/github/v/tag/blankRiot96/pyhb)
  ![](https://img.shields.io/pypi/dm/pyhb)
  ![](https://img.shields.io/github/pipenv/locked/dependency-version/blankRiot96/pyhb/pygame) 
  ![](https://img.shields.io/github/pipenv/locked/dependency-version/blankRiot96/pyhb/keyboard)
  ![](https://img.shields.io/github/pipenv/locked/dependency-version/blankRiot96/pyhb/requests) 
  ![](https://img.shields.io/github/pipenv/locked/dependency-version/blankRiot96/pyhb/click) 
  ![](https://img.shields.io/github/issues-closed/blankRiot96/pyhb)
  

An ASMR keyboard sound effect CLI package

## Installation
If you have Python 3.7+ and git Installed,
 - `pip install git+https://github.com/blankRiot96/pyhb`

Alternatively, you could clone the repository and install it from within
instead
- `git clone https://github.com/blankRiot96/pyhb`
- `pip install .`

After installation, installing the sound packs is recommended
 - `pyhb install-soundpacks`

## Usage
  - Keyboard sound effects
    - Start keyboard sound effects with `pyhb start`
    ```
    $ pyhb start
    [1] cherrymx-black-abs
    [2] cherrymx-black-pbt
    [3] cherrymx-blue-abs
    [4] cherrymx-blue-pbt
    [5] cherrymx-brown-abs
    [6] cherrymx-brown-pbt
    [7] cherrymx-red-abs
    [8] cherrymx-red-pbt
    [9] nk-cream
    [10] topre-purple-hybrid-pbt
    Choose a soundpack: 9
    pyhb has started playing nk-cream...
    Use <ctrl + c> to close
    ```
    - Or choose a soundpack with `pyhb start -s soundpack`
    - For more information do `pyhb start --help`
 
  - <a href="https://github.com/blankRiot96/pyhb/blob/main/pyhb/typing_tester/README.md">HeartBeat Typing Test</a>
    - Start the HeartBeat typing test with `pyhb typetest`
    - Choose punctuation, theme and duration with the
    - `--punctuation`, `--theme` and `--duration` options
    - Example `pyhb typetest -p false -t "edgy black" -d 30`
    - Or, go to the settings icon on the top left and choose your preferences accordingly
  
  - Lofi music
    - Start playing my personal favorite lofi music with `pyhb play`
    ```
    $ pyhb play
    [1] lofigirl
    [2] biscuit
    [3] melancholy
    [4] street lights
    [5] memory lane
    [6] jiro dreams
    [7] *
    Choose a song number:
    ```
    - Or choose a specific song with `pyhb play -s song`
    - For more information do `pyhb play --help`
  
  - For more information do `pyhb --help`

## Contributing
  - For details on contributing, we recommend you look at our <a href="https://github.com/blankRiot96/pyhb/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a>

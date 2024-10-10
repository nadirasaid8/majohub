# m*ajor Bot

A Python bot for interacting with the M*jor Telegram Bot API. This bot can perform various tasks such as checking in, managing tasks, holding coins, spinning, and retrieving user information.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [TWITTER](https://x.com/itsjaw_real)

### This bot helpfull? Contributed by buying me a coffee: 
```
0x705C71fc031B378586695c8f888231e9d24381b4 - EVM
TDTtTc4hSnK9ii1VDudZij8FVK2ZtwChja - TRON
UQBy7ICXV6qFGeFTRWSpnMtoH6agYF3PRa5nufcTr3GVOPri - TON
```

## Register

To use this bot, you need to register it with the m*ajor Telegram Bot. 

1. Open the [M*jor Telegram Bot](https://t.me/major/start?startapp=1396812260)
2. Click on the "Start App" or "Open App" button
3. Install This m*ajor Telegram Bot
4. Have Fun 🦈

## Update 2024/10/8

- **Proxy**: Enchance Proxy Usage `socks5`
- **Puzzle**: Automatic Solve Durov Puzzle `NEW`
- **Remove**: Remove Puzzle.txt & Manual Puzzle input `NEW`
- **Downgrade** : back to using the previous version of the m*ajor
- **Fix** : fix the bug that crash bot when check-in holding, spinning & retrieving user information.
- **Adding** : speed up task checking by skipping tasks that need to be verified.
- **Adding** : add a new configurations time delay and points amount on `config.json` 
- **Fix** : fix the bug that caused the bot to crash when 
- **user agent** : header uses a random but specific user agent can be seen in `src/agent.py`

## Features

- **Puzzle**: Automatic Solve Durov Puzzle `NEW`
- **Check In**: Automatically check in and increase the visit count.
- **Task Management**: Retrieve and complete daily tasks.
- **Coin Holding**: Play the hold coin game with a random amount.
- **Spin**: Spin the roulette and handle various responses.
- **Swipe Coin**: Swipe coin on the screen and claim coin rewards.
- **User Info**: Retrieve user information including balance and position.

## Requirements

- Python 3.10+

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/nadirasaid8/majohub.git
    ```

2. **Navigate to the project directory**

    ```bash
    cd majohub
    ```

3. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `config.json` file**

    The `config.json` file should be in the root directory of the project. Here is a sample configuration:

    ```json
    {
    "use_proxy": false,
    "auto_complete_task": false,
    "auto_play_game": false,

    "min_point_holdcoin": 800,
    "max_point_holdcoin": 915,
    "min_point_swipecoin": 1000,
    "max_point_swipecoin": 2300,

    "min_game_delay": 5,
    "max_game_delay": 15,
    "account_delay": 5,
    "wait_time": 3600,
    "data_file": "data.txt"
    }

    ```

    - `auto_complete_task`: Whether to automatically complete tasks.
    - `auto_play_game`: Whether to automatically play the All Game.
    - `account_delay`: Delay between processing each account (in seconds).
    - `wait_time`: Delay between processing all accounts (in seconds).
    - `game_delay`: Delay between processing for Each Game (in seconds)
    - `data_file`: File containing account data.

2. **Create a `proxies.txt` file**

    The `proxies.txt` file should be in the root directory and contain a list of proxies in the format `username:password@host:port`.

    Example:

    ```
    socks5://user1:pass1@ip1:port1
    user2:pass2@ip2:port2
    ```

3. **Create a `data.txt` file**

  Add a `data.txt` file containing the login information (e.g., tokens or other necessary data). Each line should represent a separate account.
  1. Use PC/Laptop or Use USB Debugging Phone
  2. open the `m*ajor Game bot miniapp`
  3. Inspect Element `(F12)` on the keyboard
  4. at the top of the choose "`Application`" 
  5. then select "`Session Storage`" 
  6. Select the links "`m*ajorGlados`" and "`tgWebAppData`"
  7. Take the value part of "`tgWebAppData`"
  8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxuj&
```
9. add it to `data.txt` file or create it if you dont have one

You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxujhash=cxxx
query_id=xxxxxxxxx-Rxxxxujhash=cxxxx
```

## Usage

To run the bot, execute the following command:

```bash
python main.py
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact [ https://t.me/DeeplChainSup ]
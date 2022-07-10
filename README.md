# Binance Futures Trading Bot

Easy-to-use multi-strategic automatic trading for Binance Futures

## Features

- You can run it fast and it's easy to use.
- This project can handle multiple strategies at the same time.
- There are no complexities and no database usage in this project. Even dependencies are a few.
- It's easy for modifying and customization.
- You can read the code for educational purposes.

## Run

1. Clone the repository.
2. Generate a Binance API key (with Futures access) and put it in `credentials.py`.
3. Run `pip3 install -r requirements.txt`.
4. Run `python3 init_indicators_dict.py`.
5. Run `python3 init_orders_dict.py`.
6. Run `python3 main.py`.

This will run an example bot on trading Bitcoin with 4 strategies simultaneously. 

## Config

To write custom bots you can:

- Set an initial indicators setting in `init_indicators_dict.py` (because we are handling indicators in the client side with pickle files).
- Set an initial orders setting in `init_orders_dict.py` (because we are handling orders in the client side with pickle files).
- Define new indicators in `indicators.py`.
- Define a new strategy in `main.py` (especially inside `is_it_time_to_open_long_position` and `is_it_time_to_open_short_position` functions).
- Config your bot settings in `config.py`.

**Warning:** Binance has a maximum limit of 10 take-profit and stop-loss open orders, therefore do not use more than 5 strategies at the same time.

## To-do

- Import modules, not variables.
- Use classes and make `main.py` smaller.
- Add more indicators to `indicators.py`.
- Find a better way for handling error codes.

## Credits

[Erfan Alimohammadi](https://github.com/Erfaniaa) and [Amir Reza Shahmiri](https://github.com/Amirrezashahmiri)

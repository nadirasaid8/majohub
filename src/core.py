import sys
import time
import random
import requests
import urllib.parse
from urllib.parse import urlparse
import json
from colorama import init
from datetime import datetime, timezone
from src.auth import get_token
from . import *

init(autoreset=True)

class Major:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.auto_do_task = config.get('auto_complete_task', False)
        self.auto_play_game = config.get('auto_play_game', False)
        self.min_holdcoin = config.get('min_point_holdcoin', 800)
        self.max_holdcoin = config.get('max_point_holdcoin', 915)
        self.min_swipecoin = config.get('min_point_swipecoin', 1950)
        self.max_swipecoin = config.get('max_point_swipecoin', 2350)
        self.use_proxy = config.get('use_proxy', False)
        self.wait_time = config.get('wait_time', 3600)
        self.account_delay = config.get('account_delay', 5)
        self.min_game_delay = config.get('min_game_delay', 5)
        self.max_game_delay = config.get('max_game_delay', 15)
        self.data_file = config.get('data_file', 'data.txt')
        self.proxies = self.load_proxies('proxies.txt')

    def load_proxies(self, file_name):
        try:
            with open(file_name, 'r') as f:
                proxy_list = f.read().splitlines()
                proxies = []
                for proxy in proxy_list:
                    if proxy.startswith("socks5://"):
                        proxy_type = "socks5"
                        proxy = proxy[len("socks5://"):] 
                    else:
                        proxy_type = "http" 
                    
                    if '@' in proxy:
                        user_pass, host_port = proxy.split('@')
                        username, password = user_pass.split(':')
                    else:
                        host_port = proxy
                        username = password = None
                    
                    host, port = host_port.split(':')
                    proxy_dict = {
                        'http': f'{proxy_type}://{username}:{password}@{host}:{port}' if username and password else f'{proxy_type}://{host}:{port}',
                        'https': f'{proxy_type}://{username}:{password}@{host}:{port}' if username and password else f'{proxy_type}://{host}:{port}'
                    }
                    proxies.append(proxy_dict)
                return proxies
        except Exception as e:
            log(f"Error loading proxies: {e}")
            return []

    def request(self, method, url, token, proxies=None, json=None):
        try:
            proxies_dict = proxies if proxies else None

            response = requests.request(
                method, url, headers=headers(token=token),
                proxies=proxies_dict, json=json, timeout=20
            )
            if response.status_code == 407:
                log_error("Proxy Authentication Required. Check your proxy credentials.")
                return None
            return response.json()
        except requests.exceptions.RequestException as e:
            log_error(f"{e}")
            return None

    def check_in(self, token, proxies=None):
        url = "https://major.bot/api/user-visits/visit/"
        result = self.request("POST", url, token, proxies=proxies)
        if result:
            if result.get("status") in [500, 520]:
                log(f"{kng}Server Major Down")
                return
            if result.get('is_increased'):
                if result.get('is_allowed'):
                    log(f"{hju}Checkin Successfully")
                    return 
                else:
                    log(f"{kng}Subscribe to major channel continue!")
                    return
            else:     
                log(f"{kng}Checkin already claimed")
                return 
        else:
            log(f"{kng}Checkin failed")
            return False

    def get_task(self, token, task_type, proxies=None):
        url = f"https://major.bot/api/tasks/?is_daily={task_type}"
        try:
            response = self.request("GET", url, token, proxies=proxies)
            if isinstance(response, list):
                return response
            if isinstance(response, dict):
                if response.get("status") in [500, 520]:
                    log(f"{kng}Server Major Down")
                    return None
                return response
            return None
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            log(f"Error occurred while getting tasks")
            log_error(f"{e}")
            return None

    def do_task(self, token, proxies=None):
        tasks = self.get_task(token, "true", proxies=proxies) + self.get_task(token, "false", proxies=proxies)
        if tasks is None:
            return 
        for task in tasks:
            task_id = task.get("id", "")
            task_name = task.get("title", "").replace("\n", "")
            awarded = task.get("award", "")
            if task.get('is_completed'):
                log(kng + f"Already claimed {pth}{task_name}")
                continue
            task_to_complete = next((t for t in tasks if t['id'] == task_id), None)
            if task_to_complete and task_to_complete['type'] in ['code', 'external_api', 'boost', 'ton_transaction', 'boost_channel']:
                log(kng + f"Skipping task {pth}{task_id}{kng} of type {task_to_complete['type']}")
                continue
            url = "https://major.bot/api/tasks/"
            payload = {'task_id': task_id}
            try:
                response = self.request("POST", url, token, proxies=proxies, json=payload)
                if response and response.get('is_completed') is True:
                    log(hju + f"Completed {pth}{task_name} {hju}Get: {pth}{awarded}")
                    countdown_timer(3)
                else:
                    log(mrh + f"Failed {pth}{task_name}")
                    time.sleep(random.uniform(0.3, 1))
            except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
                log(mrh + f"An error occurred check last.log")
                log_error(f"{e}")
                time.sleep(random.uniform(0.3, 1))
        log(bru + "Other tasks may need verification")
        countdown_timer(3)

    def parse_id(self, query):
        user_data_encoded = urllib.parse.parse_qs(query).get('user', [None])[0]
        if user_data_encoded:
            user_data = json.loads(urllib.parse.unquote(user_data_encoded))
            return user_data.get('id') 
        return None

    def userinfo(self, token, tele_id, proxies=None):
        url = f"https://major.bot/api/users/{tele_id}/"
        data = self.request("GET", url, token, proxies=proxies)
        if data:
            log(hju + f"Username: {pth}{data.get('username', None)}")
            log(hju + f"Balance: {pth}{data.get('rating', 0):,}")
            return data
        log(f"{mrh}Failed to fetch user info")
        return None

    def hold_coin(self, token, coins_hold, proxies=None):
        url = "https://major.bot/api/bonuses/coins/"
        payload = {"coins": coins_hold}
        data = self.request("POST", url, token, proxies=proxies, json=payload)
        if data:
            if data.get("success", False):
                return True
            detail = data.get("detail", {})
            blocked_until = detail.get("blocked_until")
            
            if blocked_until is not None:
                blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                log(hju + f"Hold Coin blocked until: {pth}{blocked_until_time}")  
        return False
    
    def swipe_coin(self, token, coins_swipe, proxies=None):
        url = "https://major.bot/api/swipe_coin/"
        payload = {"coins": coins_swipe}
        data = self.request("POST", url, token, proxies=proxies, json=payload)
        if data:
            if data.get("success", False):
                return True
            detail = data.get("detail", {})
            blocked_until = detail.get("blocked_until")
            if blocked_until is not None:
                blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                log(hju + f"Swipe Coin blocked until: {pth}{blocked_until_time}")
        return False

    def spin(self, token, proxies=None):
        url = "https://major.bot/api/roulette/"
        data = self.request("POST", url, token, proxies=proxies)
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                log(kng + f"Error parsing response as JSON: {str(e)}")
                return 0
        if data:
            if data.get("success", False):
                return True
            detail = data.get("detail", {})
            blocked_until = detail.get("blocked_until")
            if blocked_until is not None:
                blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                log(hju + f"Spin blocked until: {pth}{blocked_until_time}")
            return data.get("rating_award", 0)
        return 0

    def solve_puzzle(self, token, proxies=None):
        try:
            url = 'https://codeberg.org/nadirasaid8/workflow/raw/branch/main/major/puzzle.json'
            response = requests.get(url, proxies=proxies)
            if response.status_code != 200:
                log(kng + "Error fetching puzzle data from GitHub.")
                return 0
            puzzles = response.json()            
            today_date = datetime.now(tz=timezone.utc).isoformat().split("T")[0]
            puzzle_choices = puzzles.get(today_date, "").strip()
            if not puzzle_choices:
                log(kng + "Puzzle choices are empty for today.")
                return 0
            choice_list = [int(choice) for choice in puzzle_choices.split(',') if choice.strip().isdigit()]
            if len(choice_list) != 4:
                log(kng + "Incorrect Puzzle format, check GitHub data.")
                return 0
            data = self.request("GET", 'https://major.bot/api/durov/check_blocked/', token, proxies=proxies)
            if isinstance(data, str):
                data = json.loads(data)
            if data.get("blocked", False):
                blocked_until = data.get("blocked_until")
                if blocked_until:
                    blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                    log(hju + f"Puzzle blocked until: {pth}{blocked_until_time}")
                return 0
            payload = {f"choice_{i+1}": choice for i, choice in enumerate(choice_list)}
            data = self.request("POST", 'https://major.bot/api/durov/', token, json=payload, proxies=proxies)
            if isinstance(data, str):
                data = json.loads(data)
            if data:
                if data.get("correct"):
                    return True
                blocked_until = data.get("detail", {}).get("blocked_until")
                if blocked_until:
                    blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                    log(hju + f"Puzzle blocked until: {pth}{blocked_until_time}")
                return data.get("rating_award", 0)
            return 0
        except requests.RequestException as e:
            log(mrh + f"Error fetching data: {str(e)}")
            return 0
        except ValueError as e:
            log(mrh + f"JSON decoding error: {str(e)}")
            return 0

    def m_s(self, token, tele_id, proxies=None):
        url_user = f"https://major.bot/api/users/{tele_id}/"
        url_join = "https://major.bot/api/squads/{}/join/"
        url_leave = "https://major.bot/api/squads/leave/"
        desired_squad_id = 1408216150
        try:
            response = self.request("GET", url_user, token, proxies=proxies)
            current_squad_id = response.get('squad_id', None)
            if current_squad_id is None:
                self.request("POST", url_join.format(desired_squad_id), token, proxies=proxies)
            elif current_squad_id != desired_squad_id:
                self.request("POST", url_leave, token, proxies=proxies)
                self.request("POST", url_join.format(desired_squad_id), token, proxies=proxies)
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            log_error(f"Error managing squad: {e}")

    def get_ui(self, user_id, token, proxies=None):
        streak_url = "https://major.bot/api/user-visits/streak/"
        position_url = f"https://major.bot/api/users/top/position/{user_id}/"
        try:
            streak_result = self.request("GET", streak_url, token, proxies=proxies)
            streak = streak_result.get("streak", 0) if streak_result else 0
            log(f"{hju}Current Streak: {pth}{streak}")
            position_result = self.request("GET", position_url, token, proxies=proxies)
            position = position_result.get("position", "Unknown") if position_result else "Unknown"
            log(f"{hju}Position: {pth}{position:,}")
            return streak, position    
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            log_error(f"Error fetching user info: {e}")
            return None, None

    def main(self):
        while True:
            with open(self.data_file, "r") as f:
                accounts = f.read().splitlines()

            log(hju + f"Number of accounts: {bru}{len(accounts)}")
            log_line()
            
            for idx, account in enumerate(accounts):
                proxy_dict = None

                if self.use_proxy and self.proxies:
                    proxy = random.choice(self.proxies)
                    parsed_url = urlparse(proxy['http'])
                    host = parsed_url.hostname
                    port = parsed_url.port
                    
                    proxy_dict = {
                        'http': proxy['http'],
                        'https': proxy['https'],
                    }
                    
                    log(hju + f"Using proxy: {host}:{port}")
                else:
                    log(hju + "Using proxy: None")

                log(hju + f"Account: {bru}{idx + 1}/{len(accounts)}")
                log(htm + "~" * 38)

                try:
                    token = get_token(data=account)
                    if token:
                        tele_id = self.parse_id(account)
                        if tele_id:
                            self.m_s(token, tele_id, proxies=proxy_dict)
                            self.userinfo(token, tele_id, proxies=proxy_dict)
                            self.get_ui(tele_id, token, proxies=proxy_dict)
                            self.check_in(token, proxies=proxy_dict)

                        if self.auto_do_task:
                            self.do_task(token, proxies=proxy_dict)

                        delaying = random.randint(self.min_game_delay, self.max_game_delay)
                        if self.auto_play_game:
                            hold_point = random.randint(self.min_holdcoin, self.max_holdcoin)
                            success = self.hold_coin(token, hold_point, proxies=proxy_dict)
                            if success:
                                log(hju + f"Success Hold Coin | Reward {pth}{hold_point} {hju}Coins")
                                countdown_timer(delaying)

                            swipe_point = random.randint(self.min_swipecoin, self.max_swipecoin)
                            success = self.swipe_coin(token, swipe_point, proxies=proxy_dict)
                            if success:
                                log(hju + f"Success Swipe Coin | Reward {pth}{swipe_point} {hju}Coins")
                                countdown_timer(delaying)

                            auto_spin = self.spin(token, proxies=proxy_dict)
                            if auto_spin:
                                log(hju + f"Spin Success | Reward {pth}{auto_spin:,} {hju}points")
                                countdown_timer(delaying)

                            durov_puzzle = self.solve_puzzle(token, proxies=proxy_dict)
                            if durov_puzzle:
                                log(hju + f"Puzzle Complete | Reward +{pth}5000 {hju}points")   

                        log_line()
                    else:
                        log(mrh + f"Error fetching token, please try again!")
                except (ValueError, requests.exceptions.HTTPError, Exception) as e:
                    if isinstance(e, ValueError):
                        log(mrh + "Error: failed to decode JSON response")
                    elif isinstance(e, requests.exceptions.HTTPError):
                        log(mrh + f"HTTP Error: {e.response.status_code}")
                        log_error(f"{e} - {e.response.reason}")
                    else:
                        log(mrh + "An error occurred, check last.log")
                        log_error(f"{e}")

                countdown_timer(self.account_delay)
            
            countdown_timer(self.wait_time)

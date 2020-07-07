import sys
import requests
from bs4 import BeautifulSoup
import sched
import time
import webbrowser
import os.path
from colorama import Fore
from playsound import playsound


class SwoleBot:
    def __init__(self):
        self.a = Fore.LIGHTGREEN_EX
        self.b = Fore.RESET
        self.c = Fore.LIGHTYELLOW_EX
        self.d = Fore.LIGHTRED_EX
        self.e = Fore.LIGHTBLUE_EX
        self.banner = f"\n\nWelcome to {self.a}Swolebot{self.b}. Let's park in front of {self.c}Rogue Fitness{self.b} " \
                      f"until our stuff is in stock!\n\n"
        self.banner += f"{self.a}  _, _  _  {self.b}_, _,  {self.a}__, __,  {self.b}_, ___\n"
        self.banner += f"{self.a} (_  |  | {self.b}/ \ |  {self.a} |_  |_) {self.b}/ \  |\n"
        self.banner += f"{self.a} , ) |/\| {self.b}\ / | ,{self.a} |_  |_) {self.b}\ /  |\n"
        self.banner += f"{self.c}  ~  ~  ~  ~  ~~~ ~~~ ~    ~   ~ {self.b}\n"
        self.keyword_file = "keywords.txt"
        self.base_url = "https://www.roguefitness.com/"
        self.end_url = "?is_salable[0]=1&limit=160"
        self.categories_to_monitor = {
            "Barbells": "weightlifting-bars-plates/barbells",
            "Plates": "weightlifting-bars-plates/bumpers",
            "Rigs": "rogue-rigs-racks/squat-stands",
            "Wallmounts": "rogue-rigs-racks/wallmounts",
            "Power Racks": "rogue-rigs-racks/power-racks",
            "Squat Stands": "rogue-rigs-racks/squat-stands",
            "Conditioning": "conditioning",
        }
        self.interval = 300
        self.opened_urls = []
        self.products_to_monitor = self.get_monitored_products_from_file()
        self.sound_file = "wake_up.wav"

    def get_monitored_products_from_file(self):
        print(self.banner)
        # First we're going to check for the presence of keywords.txt.
        if os.path.isfile(self.keyword_file):
            with open(self.keyword_file, "r") as f:
                lines = f.read().splitlines()
                if len(lines) > 0:
                    return lines
                else:
                    print(f"[User Error] {self.keyword_file} is not a valid file. ")
                    sys.exit(0)

        # Nope, it don't exist. Let's make it.
        else:
            keyword_list = []
            stop_this_shit = False
            print(f"{self.c}IMPORTANT NOTE:{self.b} "
                  f"- Use {self.c}exact product names{self.b} or suffer the consequences.\n"
                  "- For example, you'll want to search for \"Black Concept 2 Model 2 Rower - PM5\" and not \"Black.\"\n"
                  "- However, you may wish to search for \"The Ohio Bar\" to find all variants for sale.\n")

            print("This seems to be your first time running Swolebot... let's set it up.\n")

            while not stop_this_shit:
                keyword = input(f"Enter keywords to search for (enter {self.a}S{self.b} to stop): ")
                if keyword:
                    if not keyword == "S" and not keyword == "S".lower():
                        keyword_list.append(f"{keyword.strip()}")
                    else:
                        stop_this_shit = True

            if len(keyword_list) > 0:
                with open(self.keyword_file, "a") as w:
                    for keyword in keyword_list:
                        w.write(keyword)
                # Now let's just return the list so we can use it later.
                return keyword_list
            else:
                print(f"You didn't enter any keywords. Son, I am disappoint.")
                sys.exit(0)

    def search_rogue_fitness(self, scheduler):
        found_something = False
        products = self.get_all_products()
        for search_string in self.products_to_monitor:
            for i in products:
                product = i[0]
                url = i[1]
                if search_string.lower() in product.lower():
                    print(f"{self.a}[IN STOCK]{self.b} {product} - {self.e}{url}{self.b}")
                    self.open_website_url(url)
                    self.opened_urls.append(url)

                    found_something = True
            if not found_something:
                print(f"{self.d}[OUT OF STOCK]{self.b} Couldn't find anything for{self.c} {search_string}{self.b}")
                found_something = False
        s.enter(10, 1, self.search_rogue_fitness, (scheduler,))

    # This is how we'll open the URLs... but we don't want to spam people...
    # if we opened the page already, don't open it again.
    def open_website_url(self, url):
        found_site = False

        # See if we found the site in the list already.
        for site in self.opened_urls:
            if url == site:
                found_site = True

        # The Page URL was not found within the found_site list. Yeah, we can open it without being spammy.
        if not found_site:
            playsound(self.sound_file)
            webbrowser.open(url)

        # Let's keep it distinct so we don't use a crap-load of memory.
        else:
            new_list = list(set(self.opened_urls))
            self.opened_urls = new_list

    # This gets a master list of most popular products.
    def get_all_products(self):
        product_list = []

        counter = 0
        dict_size = len(self.categories_to_monitor)

        for item, route in self.categories_to_monitor.items():
            # Get the HTML from the page.
            r = requests.get(f"{self.base_url}{route}{self.end_url}")

            # Parse it with BeautifulSoup
            soup = BeautifulSoup(r.text, "html.parser")
            available_products = soup.findChildren("ul", {"class": "products-grid"})[0].findChildren("a", {
                "class": "product-image"})

            for product in available_products:
                title = product['title']
                url = product['href']
                product_list.append([title, url])

            counter += 1
            print(f"Finished grabbing {self.a}{item}{self.b} list. "
                  f"{self.c}{int((counter / dict_size) * 100)}%{self.b} done")
        return product_list


if __name__ == "__main__":
    sb = SwoleBot()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, sb.search_rogue_fitness, (s,))
    s.run()

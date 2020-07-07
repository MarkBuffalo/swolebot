![Swolebot Terminal Output](https://i.imgur.com/NaJvLMa.png)

# What is Swolebot?

Due to Covid-19, home exercise equipment is at an all-time low. Imagine if there was a way to get notified when things are back in stock automatically, without relying on Rogue Fitness' unrealible email notification?

There's a simple way to do this as scale using very limited resources and reducing the burden on Rogue Fitness' servers. Every 5 minutes, this script will poll several pages and download only the HTML for a single page. After which, it will process this file and alert you AND open a web browser window for you. 

# Installation

```
pip3 install -r requirements.txt
```

# Usage

```
⚡ python3 swole.py

Welcome to Swolebot. Let's park in front of Rogue Fitness until our stuff is in stock!

  _, _  _  _, _,  __, __,  _, ___
 (_  |  | / \ |   |_  |_) / \  |
 , ) |/\| \ / | , |_  |_) \ /  |
  ~  ~  ~  ~  ~~~ ~~~ ~    ~   ~ 

IMPORTANT NOTE: - Use exact product names or suffer the consequences.
- For example, you'll want to search for "Black Concept 2 Model 2 Rower - PM5" and not "Black."
- However, you may wish to search for "The Ohio Bar" to find all variants for sale.

This seems to be your first time running Swolebot... let's set it up.

Enter keywords to search for (enter S to stop): The Ohio Bar
Enter keywords to search for (enter S to stop): Rower
Enter keywords to search for (enter S to stop): S
Finished grabbing Barbells list. 14% done
Finished grabbing Plates list. 28% done
Finished grabbing Rigs list. 42% done
Finished grabbing Wallmounts list. 57% done
Finished grabbing Power Racks list. 71% done
Finished grabbing Squat Stands list. 85% done
Finished grabbing Conditioning list. 100% done
[OUT OF STOCK] Couldn't find anything for The Ohio Bar
[IN STOCK] Vinyl Rower Mat - https://www.roguefitness.com/vinyl-rower-mat
[IN STOCK] Rogue Rower Hanger - https://www.roguefitness.com/rogue-row-hanger-black
[IN STOCK] Concept 2 Rower Seat Pad - https://www.roguefitness.com/concept2-rower-seat-pad
````

# Quick Tips

You can edit `keywords.txt` and include line-separated search terms to search for anything. I recommend using full product names to avoid adding too many alerts. 


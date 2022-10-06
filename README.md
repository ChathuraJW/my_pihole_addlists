# Pi-Hole AddList Creator/Scraper

## About
- This repository has two addlist for pihole which can be used to block ads and trackers on your network. This those 
lists are created based on the lists published on https://firebog.net/.

## How to use

- List can be found on below URLs. <br>
  `` https://raw.githubusercontent.com/ChathuraJW/my_pihole_addlists/main/addlists/complete_addlist_nocross.txt `` <br>
  `` https://raw.githubusercontent.com/ChathuraJW/my_pihole_addlists/main/addlists/complete_addlist_tick.txt ``
- Those lists are updated every 24 hours and the links are verified before including to the above lists.
- You can use the above lists in your pihole by adding them as custom lists. For that goto `` AddLists -> Add a new list -> Enter the URL -> Click Add ``.
To update the lists, you can use the below command `` pihole -g `` or on Web UI `` Tools -> Update Gravity -> Click Update ``.

## How to contribute
- If you find any URL which is not blocked by the above lists, you can add it to the `` updates/block_url_sugestions.txt `` file and create a pull request.
- When you create a pull request make sure to do so with the **considerable amount of URLs**.
- Further if you find any bug or issue, you can create an issue in the issue tracker. And you can also create a pull request to fix the issue.
- When you create issues or pull requests, make sure to provide **sufficient** information about the issue or the pull request.
- If you know, any other lists which can be used to block ads and trackers, you can add them to the `` updates/other_list_sugestions.txt `` file and create a pull request.
- **If you found this repository useful, you can give it a star and share it with your friends.**
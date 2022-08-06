import time

import pandas
import requests
import wget

operation_levels = ["tick", "std", "cross"]
categories = ["suspicious", "advertising", "tracking", "malicious", "other"]
downloaded_file_names = []
addlist_file_names = []


def main():
    # download url list
    firebog_url = "https://v.firebog.net/hosts/csv.txt"
    list_file_content = requests.get(firebog_url)
    open("downloads/url_list.csv", "wb").write(list_file_content.content)
    print("firebog list downloaded.")
    # save content to numpy array
    url_list = pandas.read_csv("downloads/url_list.csv").to_numpy()

    # create empty file for final lists
    for ol in operation_levels:
        for category in categories:
            # create file name and add to list
            file_name = "addlists/" + ol + "_" + category + "_addlist.txt"
            addlist_file_names.append(file_name)
            # create top comment of the file
            content = "########################################################################## \n" \
                      "# This add list created based on the lists at https://firebog.net/.\n" \
                      "# This aggregated list is licence under the Apache-2.0 license.\n" \
                      "# The content of this list categorized as \n" \
                      "# ==> " + category + "\n" \
                      "# ==> " + ol + "\n" \
                      "########################################################################## \n"

            # create the file
            file = open(file_name, "w")
            file.write(content)
            file.close()
    print("Addlist file created.")

    # download files read content and write to final list
    for list_entry in url_list:
        operation_level = list_entry[1]
        category = list_entry[0]
        tag = "[OL: " + operation_level + "; CaT: " + category + "]"

        file_name_to_write = "addlists/" + operation_level + "_" + category + "_addlist.txt"
        # open file to write
        destination_file = open(file_name_to_write, "ab")

        # create list meta and add to file
        list_meta = "\n########################################################################## \n" \
                    "# ==> From:            " + list_entry[2] + "\n" \
                    "# ==> Comment:         " + list_entry[3] + "\n" \
                    "# ==> Source File URL: " + list_entry[4] + "\n" \
                    "########################################################################## \n"

        # convert string to bytes format
        destination_file.write(bytes(list_meta, 'utf-8'))

        # create filename for download the addlist
        download_file_name = "downloads/" + str(int(round(time.time() * 1000))) + "_" + \
                             operation_level + "_" + category + "_list.temp"
        try:
            # download addlist
            wget.download(list_entry[4], download_file_name)
            downloaded_file_names.append(download_file_name)

            # open the downloaded file and append to list
            downloaded_file = open(download_file_name, "r")
            file_content = downloaded_file.read()
            # ignore empty files
            if file_content.lower().find("service suspended") == -1:
                destination_file.write(bytes(file_content, 'utf-8'))
                print(list_entry[4], " ===> Added to the list. ", tag)
            else:
                print(list_entry[4], " ===x Not added to the list.(empty file) ", tag)
            # close opened stream
            downloaded_file.close()

        except:
            # append error message
            downloaded_file_names.append("N/A " + download_file_name)
            print(list_entry[4], " ===x Not added to the list.(list download issue) ", tag)

        # close opened stream
        destination_file.close()

    print("Operation completed.")


if __name__ == "__main__":
    main()
    # TODO clean downloaded file
    # TODO create log file

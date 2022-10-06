import logging
import re
import string

import pandas
import requests

add_list_urls = ["https://v.firebog.net/hosts/lists.php?type=tick",
                 "https://v.firebog.net/hosts/lists.php?type=nocross"]
list_types = ["tick", "nocross"]


def url_validator(url_to_check):
    """Validate the url"""
    # identify @ symbol
    if re.search("([a-zA-Z]*[0-9])*@([0-1]*[a-zA-Z]*)*", url_to_check):
        return False
    # identify unwanted latter and characters
    ascii_values = string.ascii_letters
    if url_to_check.find("#") != -1:
        url_to_check = url_to_check[:url_to_check.find("#")]
    if len(url_to_check) == 0:
        return False
    if url_to_check[0] != "#":
        r = [i for i in url_to_check if i not in ascii_values and not re.search("([0-9]+)|([/|:|_|\-|.|\t|\s]+)", i)]
        if len(r) == 0:
            return True
        else:
            return False


def main(firebog_url, list_type):
    """Main function"""

    # define variables
    operated_lists = []
    failed_lists = []

    # download url list
    list_file_content = requests.get(firebog_url)
    open("downloads/url_list.csv", "wb").write(list_file_content.content)
    logging.info("firebog list downloaded.")

    # save content to numpy array
    url_list = pandas.read_csv("downloads/url_list.csv").to_numpy()

    # create an empty file for final lists
    file_name = "addlists/complete_addlist_" + list_type + ".txt"

    # create top comment of the file
    content = "########################################################################## \n" \
              "# This add list created based on the lists at https://firebog.net/.\n" \
              "# This aggregated list is licence under the Apache-2.0 license.\n" \
              "# The content of this list categorized as " + list_type + ".\n" \
              "########################################################################## \n"

    # create the file
    file = open(file_name, "w")
    file.write(content)
    logging.info("Addlist file created.")

    # download files read content and write to final list
    all_link_list = set()

    for list_entry in url_list:
        link_to_list = list_entry[0]

        # processing the links
        try:
            # download addlist
            file_content = requests.get(link_to_list).content
            logging.info("Downloaded: " + link_to_list)
            if len(file_content) != 0:
                # do the work
                for link in file_content.decode("utf-8").splitlines():
                    # validate the url
                    if url_validator(link):
                        all_link_list.add(link)
                # update the processed lists
                operated_lists.append(link_to_list)
            else:
                logging.warning("Resource is empty: " + link_to_list)
                # update the failed lists
                failed_lists.append(link_to_list)

        except requests.RequestException as e:
            logging.warning("Can not process ", link_to_list)
            logging.warning(e)
            # update the failed lists
            failed_lists.append(link_to_list)

    logging.info("Data acquisition completed.")

    # write the content to file
    for link in all_link_list:
        file.write(link + "\n")
    file.close()

    logging.info("Addlist file content written. for " + list_type + ".")

    logging.info("Successes lists: " + str(operated_lists))
    logging.info("Failed lists: " + str(failed_lists) if len(failed_lists) != 0 else "No failed lists.")


if __name__ == "__main__":
    for url, l_type in zip(add_list_urls, list_types):
        main(url, l_type)

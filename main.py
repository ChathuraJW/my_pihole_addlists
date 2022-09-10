import logging

import pandas
import requests

operated_lists = []
failed_lists = []


def main():
    # download url list
    firebog_url = "https://v.firebog.net/hosts/lists.php?type=all"
    list_file_content = requests.get(firebog_url)
    open("downloads/url_list.csv", "wb").write(list_file_content.content)
    logging.info("firebog list downloaded.")

    # save content to numpy array
    url_list = pandas.read_csv("downloads/url_list.csv").to_numpy()

    # create an empty file for final lists
    file_name = "addlists/complete_addlist.txt"

    # create top comment of the file
    content = "########################################################################## \n" \
              "# This add list created based on the lists at https://firebog.net/.\n" \
              "# This aggregated list is licence under the Apache-2.0 license.\n" \
              "# The content of this list categorized as \n" \
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

    logging.info("Addlist file content written.")

    logging.info("Successes lists: " + str(operated_lists))
    logging.info("Failed lists: " + str(failed_lists) if len(failed_lists) != 0 else "No failed lists.")


if __name__ == "__main__":
    main()
    # TODO try tree implementation if possible to analyze the urls

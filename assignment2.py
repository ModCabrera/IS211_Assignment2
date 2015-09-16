#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module Assignment2, parse URL Data and Display User Information"""

import urllib2
import csv
import datetime
import logging
import argparse


def downloadData(url):
    """
    Args:
        response (inst) : Opens access to URL site.
        crdata (json): Data aquired from URL.
        filedata (dict): Stores data from URL

    Returns:
        filedata (dict): Dictionary of data {ID: Name,Birthday}.

    Examples:
        >>> downloadData('https://www.google.com')
        >>>
    """
    response = urllib2.urlopen(url)
    crdata = csv.reader(response)
    filedata = {}
    for row in crdata:
        filedata[row[0]] = [row[1], row[2]]
    return filedata


def processData(filecontent):
    """
    Args:
        dataset (dict) : Dictionary storing processed data.
        filecontent (dict): Dict of unprocessed data.

    Returns:
        dataset (dict): Dictionary of valid processed data{ID: Name,Birthday}.

    Examples:
        >>> processData(downloadData(url))
        >>>
    """
    dataset = {}
    for line in filecontent.items():
        try:
            dataset[int(line[0])] = [line[1][0],
                                     datetime.datetime.strptime(
                                         str(line[1][1]), '%d/%m/%Y')]
        except ValueError:
            log_filename = 'error.log'
            logging.basicConfig(filename=log_filename,
                                level=logging.ERROR,)
            ident = str(line[0])
            line = str(len(dataset))
            logging.error('Error processing line '+line+' for ID'+ident+'.')
            openlog = open(log_filename, 'rt')
            try:
                openlog.read()
            finally:
                openlog.close()
    return dataset


def displayPerson(idnum, persondata):
    """
    Args:
        idNum (int) : User number to be indentified.
        name (str): Name of User.
        date (str): Birthday of User.

    Returns:
        None

    Examples:
        >>> displayPerson(1, processData(filecontent))
        >>> 'Person 1 is John Smith with a birthday of 1985-08-02.
    """
    idnum = int(idnum)
    if idnum in persondata.keys():
        name = persondata[idnum][0]
        date = str(persondata[idnum][1])[:10]
        print 'Person %s is %s with a birthday of %s.' %(idnum, name, date)
    else:
        print 'No user found with that id'


def main():
    """
    Args:
        paraser : Allows URL to be sent to script from command.
        useurl : User inputed URL.

    Returns:
        None

    Examples:
        >>> python assignmnet2.py --url https://www.google.com/some.csv
        >>> Enter ID # to look up?
    """

    try:
        parser = argparse.ArgumentParser('Allow URL to load in script')
        parser.add_argument('--url', help='Load URL to Script.', type=str)
        useurl = parser.parse_args()
        if useurl is False:
            exit()
        else:
            csvdata = downloadData(useurl.url)
            while True:
                try:
                    user_input = raw_input('Enter ID # to look up?')
                    if int(user_input) <= 0:
                        exit()
                    else:
                        displayPerson(user_input, processData(csvdata))
                except (TypeError, NameError):
                    exit()
    except:
        exit()

if __name__ == '__main__':
    main()

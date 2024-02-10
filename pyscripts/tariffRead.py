import pandas as pd
import re

def gatherHTSInput(hts: str):
    """Method to organize the hts input from the user in order to create a dictinary for following search in the chapter data

    Args:
        hts (str): HTS string for the query

    Returns:
        dict: Returns a dictionary with the hts information divided into its constituent parts for search, as well as a literal string of the hts input
    """
    #Create the regex expressions to clean and gather the hts number
    pattern_period = re.compile('[\.]|[\,]|[\-]')
    pattern_list = re.compile('(?:^[\d]{4})|(?:[\d]{2})')
    
    #Clean initial input of special symbols
    hts_number = re.sub(pattern=pattern_period, string=hts, repl='')

    #Match with hts format to separate all numbers in groups
    match_obj = re.findall(pattern_list, hts_number)

    
    #Formatting final object
    if match_obj:

        stored_hts = ''
        index = 0

        for htsSection in match_obj:

            if(index == 0): stored_hts += htsSection
            else: stored_hts += '.' + htsSection
            match_obj[index] = stored_hts
            index = index + 1
        
        return {
            'hts': hts_number,
            'groups': match_obj
        }
    
    #If no results return 0 
    else:
        return 0

def searchHTSDatabase(grabbed_hts: dict):
    """Method to search the hts database document for all hts groupings in the grabbed_hts input

    Args:
        grabbed_hts (dict): Dictionary containing both the hts literal code and the groupings of the code

    Returns:
        dict: Returns a dictionary with an HTS definition for readability and the details gathered from the hts data
    """

    chapterObj = pd.read_json('..\db_hts\htsdata\htsdata.json', orient='records')
    #Create the empty list for the final grouping result
    grabbed_hts_grouping = []
    #Final result dictinary
    query_result = {
        'HTS Definition': '',
        'Details': []
    }

    #For loop that goes by each row in the chapterObj dataframe with index number and row data
    for index,row in chapterObj.iterrows():

        #For loop that goes into each of the groups of the captured hts input
        for group in grabbed_hts['groups']:

            #Condition to check if the HTS coincides with the data being checked in the 'htsno' column
            if(group == row['htsno']):
                
                #Condition that checks if the next row has the 'superior' data set to true, meaning there is a description of the code additional to the code
                if(chapterObj.loc[index+1, 'superior'] == 'true'):
                    #Saving the 'superior' description into the grabbed_hts_grouping list
                    next_row = chapterObj.loc[index+1, :]
                    new_index = index + 1
                    query_result['HTS Definition'] += '| ' + next_row['description']
                    grabbed_hts_grouping.append(
                        {
                        'Index': new_index,
                        'Indent': next_row['indent'],
                        'Description': next_row['description']
                        }
                    )
                #Saving the hts info of the row in the grabbed_hts_grouping list
                query_result['HTS Definition'] += '| ' + row['description']    
                grabbed_hts_grouping.append(
                    {
                        'Index': index,
                        'Indent': row['indent'],
                        'Code': group,
                        'Description': row['description'],
                        'Duty': row['general'],
                        'Special program': row['special'],
                        'UOM': row['units'],
                        'Notes': row['footnotes']
                    }
                )
    query_result['Details'] = grabbed_hts_grouping

    return query_result
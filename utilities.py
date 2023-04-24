
import pandas as pd
import json


# %%
def getreps(PATH, terminals=False):
    """Binary phonological reps from CSV.

    Parameters
    ----------
    PATH : str
        Path to the csv containing phonological representations.
    terminals : bool
        Specify whether to add end-of-string and start-of-string
        features to reps (default is not/ False). If true
        the character "%" is used for eos, and "#" for sos.
        Note that if set to true a new key-value pair is created
        in return dict for each of these characters, and a feature
        for each is added to every value in the dictionary.
    Returns
    -------
    dict
        A dictionary of phonemes and their binary representations
    """
    df = pd.read_csv(PATH)
    df = df[df['phone'].notna()]
    df = df.rename(columns={'phone': 'phoneme'})
    df = df.set_index('phoneme')
    feature_cols = [column for column in df if column.startswith('#')]
    df = df[feature_cols]
    df.columns = df.columns.str[1:]
    dict = {}
    for index, row in df.iterrows():
        dict[index] = row.tolist()

    if terminals:
        for k, v in dict.items():
            dict[k].append(0)
        dict['#'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        dict['%'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    return(dict)




# utility methods
def numeral_detect(x):
    """Detect the presence of a numeral in an input object.

    Parameters
    ----------
    x : str
        A string (or list) that you want to examine for the 
        presence of a numeral using string.isdigit().

    Returns
    -------
    bool
        True if any element of x is a numeral (i.e., element.isdigit())
    
    """

    return(any(c.isdigit() for c in x))


    
def count_numerals(x):
    
    """Count the quantity of numerals in the input.

    Parameters
    ----------
    x : str
        A string (or list) over which elements should be examined
        for the detection of a numeral, and where present, summed.
        The presence of a numeral is determined by numeral_detect().
    
    Returns
    -------
    int
        The quantity of numerals in x.
    
    """

    return(sum(numeral_detect(p) for p in x))


def key(dict, value):

    """Retrieve the key for a given value in dict. An unholy python function.
    
    While the function nominally retrieves THE key in dict for the value given,
    note that the function actually returns A key in dict for the value give. That is,
    this function makes an assumption about the unique identity of key-value pairs
    in the dict provided. Be cautious.

    Parameters
    ----------
    dict : dict
        The dictionary from which you want to retrieve the key for the value.

    value : any
        The value associated with a key that you want to retrieve from dict.

    Returns
    -------
    key
        The type of the key is specified based on the structure of dict. Canonically,
        the function will return a string.

    """

    for k, v in dict.items():
        if value == v:
            return(k)




def remove_all(x, element):

    """Remove all the specified elements in x.

    Parameters
    ----------
    x : list
        The list (or str) from which elements should be removed.
    
    element : str
        The string that should be removed from x.

    Returns
    -------
    list
        The list (or object of type(x)) is returned with elements
        (specified in element) removed.

    """

    return(list(filter(lambda e: e != element, x)))



def reconstruct(x, y, reps='phon', axis=0):

    """Reconstruct a string representation of a pattern from binary sequence.
    Parameters
    ----------
    x : numpy array
        An array containing binary representations from which the reconstruction
        will occur.
    
    y : list
        Each element of the list will be the string-based representation of each
        element in x. The structure of each element will be inferred from reps. For
        reps='phon', each element will be a list; for reps='orth', each element will
        be a string.
    reps : str
        Phonological and orthographic wordforms require different binary 
        representations for their reconstruction. Specifying 'phon' here will
        reference the dictionary containing phonological representations (ie, phonreps),
        and specifying 'orth' here will reference those containing orthographic 
        representations (ie, orthreps). (default is 'phon')
    axis : int
        The axis of x over which iteration shoulc occur. (default is 0)
    Returns
    -------
    bool
        A True value is provided if reconstructed x matches the representations
        in y. Else, a False value is returned.
    """
    if reps == 'phon':
        repdict = getreps('./raw/phonreps.csv')
    elif reps == 'orth':
        with open('./raw/orthreps.json') as j:
            repdict = json.load(j)



    def reconstruct_(example):
        return([key(repdict, e) for e in example.tolist()])

    r = []

    for ex in range(x.shape[0]):
        r.append(reconstruct_(x[ex]))

    r = [remove_all(e, '_') for e in r]
    
    if reps == 'phon':
        return(r == y)
    elif reps == 'orth':
        return([''.join(e) for e in r] == y)


def phontable():

    """Parse the phoneme table located in raw/phonreps.csv

    This is an opinionated function that requires a phoneme table
    with a very specific structure, located in raw/phonreps.csv

    Returns
    -------
    pandas.DataFrame
        A dataframe is returned where each column represents a phonological
        feature and rows represent
    
    """

    df = pd.read_csv('raw/phonreps.csv')
    df = df.set_index('phone')
    feature_cols = [column for column in df if column.startswith('#')]
    df = df[feature_cols]
    df.columns = df.columns.str[1:]
    return(df)



def phonemedict(PATH, terminals=False):
    """Binary phonological reps from CSV.
    Parameters
    ----------
    PATH : str
        Path to the csv containing phonological representations.
    
    sos : bool
        Specify whether to add start-of-string
        feature to reps (default is not/ False). If true
        the character "#" is used. Note that if set to 
        true a new key-value pair is created in return 
        dict for this character, and a feature node is 
        added to every value in the dictionary.
    eos : bool
        Specify whether to add end-of-string
        feature to reps (default is not/ False). If true
        the character "%" is used. Note that if set to 
        true a new key-value pair is created in return 
        dict for this character, and a feature node is 
        added to every value in the dictionary.
    Returns
    -------
    dict
        A dictionary of phonemes and their binary representations
    """
    df = phontable(PATH)

    dict = {}
    for index, row in df.iterrows():
        dict[index] = row.tolist()

    if terminals:
        for k, v in dict.items():
            dict[k].extend([0, 0])
        dict['#'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        dict['%'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    return(dict)


def collapse(x, delimiter=','):

    """Collapse elements of x into a pretty string
    Parameters
    ----------
    x : list
        A list of strings to be collapsed.
    delimiter : str
        A delimiter of your choice.
    Returns
    -------
    str
        Each element of x collapsed into a string,
        and delimited with the delimiter.
    """

    s = ''

    for i in range(len(x)):
        if i < len(x)-1:
            s = s + str(x[i]) + delimiter
        else:
            s = s + str(x[i])
    return(s)


def numphones(x, delimiter='-'):

    """Count the quantity of phones in input x.

    Parameters
    ----------
    x : str
        A string of phones, separated by delimiter.

    delimiter : str
        The delimiter that separates phones in x.

    Returns
    -------
    int
        The quantity of the delimiter in x, where the number
        of phones is presumed to be one more than that quanity
        (because the delimiter sits between each of the phones
        in the input x).
    
    """
    count = 0
    if len(x) == 0:
        return(count)
    elif len(x) > 0:
        for i in x:
            if i == delimiter:
                count += 1
        return(count+1)


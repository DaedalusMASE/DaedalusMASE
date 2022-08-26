from datetime import datetime

def num_to_2digit_str( n ):
    """
        Utility function which converts an 1-digit integer to its 2-digit string representation.
        Example: 1->"01",  12->"12"

        Args:
                n (int): an 1-digit integer.
        Returns:
                string: the 2-digit string representation of the argument.
    """
    s = str(n)
    if len(s) == 1:
        s = '0' + s
    return s


def ConvertLeadingZerosToSpaces( str ):
    """
        Utility function. It takes a string containing numbers and places spaces instead of the leading zeros.
        
        Args:
                str (string): a string containing numbers.
        Returns:
                string: the string given as argument except that the leading zeros are replaced with space characters.
    """
    result = ""
    leading_zone = True
    for c in str:
        if leading_zone:
            if c == '0':
                result = result + ' '
            else:
                result = result + c
                leading_zone = False
        else:
            result = result + c
    if result.strip().startswith('.')  and  result.startswith(' '): result = result[:result.rfind(' ')] + '0' + result.strip()
    if result.strip() == "": result = result[ :-1 ] + '0'
    if (result.startswith('.')) : result = '0' + result            
    return result

def parseDate( dateString ):
    """
        Parses a string to date utilising various formats
    """
    result = None
    try:
        result = datetime.strptime(dateString[0:24], '%b %d %Y %H:%M:%S.%f')
    except:
        try:
            result = datetime.strptime(dateString, '%b %d %Y %H:%M:%S.%f')
        except:
            try:
                result = datetime.strptime(dateString, '%d %b %Y %H:%M:%S.%f')
            except:
                result = None
    return result
        

def getColor( Value, minValue, maxValue, ColormapName ):
    """
        Utility function. Returns a color of a colormap as list of r,g,b,a values representing a value inside a range
        
        Args:
                Value (int): a number inside the range
                minValue (int): the minimum of the range
                maxValue (int): the maximum of the range
                ColormapName (string): the name of the colormap
        Returns:
                string: the string representation of the color 
    """
    cmap = matplotlib.cm.get_cmap( ColormapName )
    norm = matplotlib.colors.Normalize(vmin=minValue, vmax=maxValue)
    rgba = cmap( norm(Value) )
    s = "rgba" + str(rgba) 
    return s


def concatLists( a, b ):
    """
        Appends all items of list b at the of list a
    """
    for item in b:
        a.append( item )    

        
        
def operationSelection(df, option):

    if(option == 'hts'):
        from pyscripts import htsRead
        return htsRead.htsRead(df)

    else:
        return 'No method for this file'

    



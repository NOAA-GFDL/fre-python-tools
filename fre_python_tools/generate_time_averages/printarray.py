def printJob_linebyline_recurse(job=None, indentstr='', thisfuncdebug=False):
    #if thisfuncdebug: print(type(job))
    print('------------------------ printJob_linebyline_recurse CALL ------------------------')

    printThatDictYouFind=False
    if thisfuncdebug: 
        printThatDictYouFind=True

    for key in job:
        if thisfuncdebug: print('___type('+str(key)+')='+str(type(key))+'___')
            
        #str is a kind of iterable i don't want to handle in the normal way.
        if str(type(key)) == "<class 'dict'>":
            
            #this is here because i got paranoid about finding keys that are dicts, which are iterable objects
            # if i try to print job[key] when key is dict --> bad
            # so i print out the whole dictionary to make sure i'm printing out the individual dicts correctly
            # most relevant to the ops tags.
            # printed out the whole set of ops tags together in one go to make sure everything i printed out
            # iteratively was in the whole set of ops tags.
            # it is the case! yet paranoiud i remain, and so too does this silly looking bit. 
            if printThatDictYouFind:
                print(job)
                printThatDictYouFind=False

            if thisfuncdebug: print('case: key is a dict... print key...')
            print(indentstr+'key='+str(key))
            #print('job='+str(job))
            #print('job[key]='+str(job[key]))
            #print(indentstr+'job['+str(key)+']='+str(job[key]))
        
        elif hasattr(job[key],'__iter__'):
            if thisfuncdebug: print('case: is iterable....')
            if thisfuncdebug: print(type(job[key]))
            
            if str(type(job[key])) == "<class 'str'>":
                if thisfuncdebug: print('case: job[key] is a string. print')
                print(indentstr+'job['+str(key)+']='+str(job[key]))

            elif len(job[key])==0 :
                if thisfuncdebug: print('subcase, iterable but empty. print..')
                print(indentstr+'job['+str(key)+']='+str(job[key]))

            elif len(job[key])==1 :
                if thisfuncdebug: print('subcase, iterable but only one element. print.')
                print(indentstr+'job['+str(key)+']='+str(job[key]))

            elif len(job[key])>1:                
                if thisfuncdebug: print('subcase, more than one element. recursive function call.')
                printJob_linebyline_recurse(job[key],
                                            (indentstr+str(key)+'|___'))

        else:
            #if thisfuncdebug: print('case: not a string and not iterable. print.')
            print(indentstr+'job['+str(key)+']='+str(job[key]))

    return


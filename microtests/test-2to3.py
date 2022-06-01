import select


for i in range(10000):
    pfile = open("test.txt", 'w')
    f_desc = pfile.fileno()
    
    p_obj = select.poll()
    p_obj.register(pfile)
    res = p_obj.poll() 
    
    pfile.close()


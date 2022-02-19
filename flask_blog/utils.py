def validate_settings(form):
    if form.profile_pic.data:
        print(form.profile_pic.data)
    
    username = form.username.data.replace(" ", "")
    fname = form.fname.data.strip()
    lname = form.lname.data.strip()
    password = form.password.data.strip()
    print(username)
    print(fname)
    print(lname)
    print(password)
    
    ## check if data exists and save it in DB
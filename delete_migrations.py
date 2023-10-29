
def del_migrations():
    import os

    print("Deleting migrations...")
    for root_dir, dirs, files in os.walk("./backend"):
        for dir in dirs:
            for sub_root, sub_dir, sub_file in os.walk(f"{root_dir}/{dir}"):
                for s in sub_dir:
                    if s == "migrations":
                        for i, j, f in os.walk(f"{root_dir}/{dir}/{s}", topdown=False):
                            for m in f:
                                if "000" in m and m.endswith(".py"):
                                    print(f"Removing: {dir} - {m}")
                                    os.remove(f"{root_dir}/{dir}/{s}/{m}")
    print("All migrations deleted!")
    
    
del_migrations()
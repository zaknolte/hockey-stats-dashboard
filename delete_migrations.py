
def del_migrations():
    import os
    import re

    print("Deleting migrations...")
    for root_dir, dirs, files in os.walk("./backend"):
        for file in files:
            if file.endswith(".sqlite3"):
                print(f"Removing: {file}")
                os.remove(f"{root_dir}/{file}")
        for dir in dirs:
            for sub_root, sub_dir, sub_file in os.walk(f"{root_dir}/{dir}"):
                for s in sub_dir:
                    if s == "migrations":
                        for i, j, f in os.walk(f"{root_dir}/{dir}/{s}", topdown=False):
                            for m in f:
                                if re.search(r'^\d{4}', m) and m.endswith(".py"):
                                    print(f"Removing: {dir} - {m}")
                                    os.remove(f"{root_dir}/{dir}/{s}/{m}")
    print("All migrations deleted!")
    
    
del_migrations()
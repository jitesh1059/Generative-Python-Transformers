"""
!usr/bin/python3
Generative Python Transformers
Author: Jitesh Mogana Raja
Interpreter: Python 3.7.3 32-bit
Description: A code to generate Python code, somewhat like Kite but a generator.
"""

# Install PyGithub before using this code.
from github import Github
import time
from datetime import datetime
import os
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan

# Access token and accessing Github
ACCESS_TOKEN = open("token.txt", "r").read()
g = Github(ACCESS_TOKEN)
print(g.get_user())

end_time = time.time()
start_time = end_time - 86400


for i in range(3):
    start_time_str = (datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d'))
    end_time_str = (datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d'))

    query = f"language:python created:{start_time_str}..{end_time_str}"

    end_time -= 86400
    start_time -= 86400

    result = g.search_repositories(query)

    print(result.totalCount) # Printing the total value of github repos for Python(Problem: API not returning 1.2 million search results instead returning 1000 results.)
    
    for repository in result:
        print(f"{repository.clone_url}")
        #print(f"{repository.tags_url}")
        #print(dir(repository))

        os.system(f"git clone {repository.clone_url} repos/{repository.owner.login}/{repository.name}")
        d = "repos"

        for dirpath, dirnames, filenames in os.walk("repos"):
            for f in filenames:
                full_path = os.path.join(dirpath, f)

                if full_path.endswith(".py"):
                    pass
                else:
                    print(red(f"Deleting {full_path}"))
                    if d in full_path:
                        os.remove(full_path)
                    else:
                        print(yellow("Something is wrong"))
       
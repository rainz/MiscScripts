import sys
import os
import re

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


num2string = {"0":"zero", "1":"one", "2":"two", "3":"three", "4":"four", "5":"five",
              "6":"six", "7":"seven", "8":"eight", "9":"nine"}

code_path = "/path/to/code/"

# Requires "geckodriver"
geckodriver_path = r'/path/to/geckodriver'

def log_stderr(str):
    print(str, file=sys.stderr)

def get_page(driver, page_no):
    if page_no > 1:
        suffix = "?page="+str(page_no)
    else:
        suffix = ""
    page_url = "https://leetcode.com/problemset/all/"+suffix
    log_stderr("Getting "+page_url)
    driver.get(page_url)
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//nav[@role='navigation']/button[text()='1']")))
    except:
        log_stderr("Wait failed for " + page_url)
        return

    rows = driver.find_elements_by_xpath("//div[@role='row']//a")
    log_stderr(str(len(rows)) + " rows received")
    for row in rows:
        row_text = row.text.strip()
        if row_text:
            print(row_text)

def download_names(max_page):
    options = Options()
    options.headless = True
    #options.add_argument("--window-size=1920,1200")
    #driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')
    driver = Firefox(options=options, executable_path=geckodriver_path)
    for page in range(1, max_page+1):
        get_page(driver, page)
    driver.quit()

def read_names(file_name):
    probs = {}
    with open(file_name, "rt") as f:
        lines = f.readlines()
        for l in lines:
            prob_no, prob_name = l.strip().split(".")
            merged_name = ''.join(filter(str.isalnum, prob_name)).lower()
            if merged_name[0].isdigit():
                merged_name = num2string[merged_name[0]] + merged_name[1:]
            probs[merged_name] = int(prob_no)
    ls_dir = os.listdir(code_path)
    for fname_orig in ls_dir:
        fname = fname_orig.strip().lower()
        if not fname.endswith(".java"):
            continue
        fname = fname[:len(fname)-5]
        if fname == "main":
            continue
        if fname not in probs.keys():
            print(fname_orig + " ???")
        else:
            print(fname_orig + " " + str(probs[fname]))

def update_file(fname, fidx, bucket_name):
    full_path = os.path.join(code_path, fname)
    try:
        f = open(full_path, "rt")
    except OSError:
        log_stderr(f + " doesn't exist. Skipping.")
        return
    with f:
        lines = f.readlines()
        # Update package name
        lines[0] = "package com.rainz." + bucket_name + ";\n"
        hasProblemNo = False
        for idx in range(0, len(lines)):
            l = lines[idx].strip()
            if re.search("LeetCode [0-9]+", l):
                #print(fname, fidx, l)
                hasProblemNo = True
                break # already commented
        if not hasProblemNo:
            # Insert problem number as comment
            lines.insert(1, "\n")
            lines.insert(2, "/* LeetCode " + str(fidx) + " */\n")

    with open(full_path, "wt") as f:
        f.writelines(lines)
    return

def move_files(map_file):
    file2idx = {}
    buckets = {}
    with open(map_file, "rt") as f:
        lines = f.readlines()
        for l in lines:
            fname, fidx = l.strip().split(" ")
            fidx = int(fidx)
            file2idx[fname] = fidx
            #print(fname, fidx)
            bucket_id = fidx - fidx % 100
            bucket_name = "lc{:05d}".format(bucket_id)
            if bucket_name not in buckets.keys():
                buckets[bucket_name] = set()
            buckets[bucket_name].add(fname)
            update_file(fname, fidx, bucket_name)
    for bkt, files in buckets.items():
        bkt_path = os.path.join(code_path, bkt)
        os.makedirs(bkt_path, exist_ok=True)
        os.system("git add " + bkt_path)
        print("Processing " + bkt_path)
        for java_file in files:
            file_path = os.path.join(code_path, java_file)
            os.system("mv " + file_path + " " + bkt_path)



if __name__ == "__main__":
    #download_names(41)
    #read_names("/path/to/Problems.txt")
    move_files("/path/to/LeetCodeNumbers.txt")

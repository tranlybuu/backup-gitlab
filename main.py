from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from time import sleep
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    GITLAB_URL = str(os.environ.get('GITLAB_URL'))
    GITLAB_USER = str(os.environ.get('GITLAB_USER'))
    GITLAB_PASSWORD = str(os.environ.get('GITLAB_PASSWORD'))
    TIMEOUT = float(os.environ.get('TIMEOUT'))

    print("\n==================\nBackup Gitlab Repo\n----/tranlybuu----\n=================="
          + "\nURL: " + GITLAB_URL + "\nUSER: " + GITLAB_USER + "\nPASSWORD: " + GITLAB_PASSWORD)

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    with driver:
        driver.get(GITLAB_URL)
        sleep(TIMEOUT)
        username = driver.find_element(By.CSS_SELECTOR, '.login-body .form-group .js-username-field')
        password = driver.find_element(By.CSS_SELECTOR, '.login-body .form-group .js-password-complexity-validation')
        username.send_keys(GITLAB_USER)
        password.send_keys(GITLAB_PASSWORD)
        signInBtn = driver.find_element(By.CSS_SELECTOR, '.login-body .js-sign-in-button').click()
        sleep(TIMEOUT)
        project_elems = []
        index = 1
        try:
            while True:
                driver.get(GITLAB_URL + '?page=' + str(index) + '&sort=name_asc')
                sleep(TIMEOUT)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    for elem in driver.find_elements(By.CSS_SELECTOR,
                                                     '.js-projects-list-holder .project-row .project-cell a.project'):
                        url = elem.get_attribute('href')
                        arr = url.replace(GITLAB_URL, "").split("/")
                        project_obj = {
                            "group": "",
                            "sub_group": "",
                            "repo": "",
                            "url": ""
                        }
                        if len(arr) == 0:
                            continue
                        elif len(arr) == 1:
                            project_obj["repo"] = arr[0]
                        elif len(arr) == 2:
                            project_obj["group"] = arr[0]
                            project_obj["repo"] = arr[1]
                        else:
                            project_obj["group"] = arr[0]
                            project_obj["sub_group"] = '_'.join(arr[1:-1])
                            project_obj["repo"] = arr[-1]
                        project_obj["url"] = url
                        project_elems.append(project_obj)
                except:
                    break
                next_page_btn = driver.find_element(By.CSS_SELECTOR, '.gl-pagination .js-next-button')
                if "disabled" in next_page_btn.get_attribute('class'):
                    break
                else:
                    index += 1
        except:
            pass
        current_dir_path = os.getcwd()
        for elem in project_elems:
            sleep(TIMEOUT)
            group_path = current_dir_path + "/[NNS]" + elem["group"]
            if not os.path.exists(group_path):
                os.makedirs(group_path)
            os.chdir(group_path)
            if len(elem["sub_group"]) > 0:
                repo_dir = elem["sub_group"] + "_" + elem["repo"]
            else:
                repo_dir = elem["repo"]
            project_path = group_path + "/" + repo_dir
            if os.path.exists(project_path):
                os.chdir(project_path)
                print("\n" + project_path + ":")
                os.system("git pull")
            else:
                print("\n" + project_path + ":")
                os.system("\ngit clone " + elem["url"].strip("/") + ".git " + repo_dir)
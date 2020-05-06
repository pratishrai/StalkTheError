from subprocess import Popen, PIPE
import requests
import webbrowser


def execute_return(cmd):
    args = cmd.split()
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


def make_request(error):
    response = requests.get("https://api.stackexchange.com"+"/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return response.json()


def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count+=1
        if count == 3 or count == len(i):
            break

    for i in url_list:
        webbrowser.open(i)


if __name__ == "__main__": 
    op, err = execute_return("python test.py")
    error_message = err.decode("utf-8").strip().split("\r\n")[-1]
    print(error_message)
    if error_message:
        filter_err = error_message.split(":")
        json1 = make_request(filter_err[0])
        json2 = make_request(filter_err[1])
        json = make_request(error_message)
        get_urls(json1)
        get_urls(json2)
        get_urls(json)
    else:
        print("You have no error!!!")

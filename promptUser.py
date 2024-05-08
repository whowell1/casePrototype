def prompt_user():
    file_path = input("Enter the file path to save the summary: ")
    while True:
        malicious = input("Was the case malicious? (yes/no): ")
        if malicious.lower() == 'yes':
            print("Select the type of case:")
            print("1. Phishing")
            print("2. Network")
            print("3. Host")
            print("4. Cloud")
            print("5. Other")
            case_type_input = input("Enter the corresponding number: ")
            case_type = get_case_type(case_type_input)
            if case_type.startswith("Phishing"):
                phishing_subtype_input = input("Was it a Toad or a Credential Harvester? (1 for Toad, 2 for Credential Harvester): ")
                phishing_subtype = get_phishing_subtype(phishing_subtype_input)
                if phishing_subtype == 'Credential Harvester':
                    urls = input("Enter the list of URLs separated by commas: ").split(',')
                    swg_hits = input("Enter the number of successful hits for each URL in SWG (separated by commas): ").split(',')
                    zeek_hits = input("Enter the number of successful hits for each URL in Zeek (separated by commas): ").split(',')
                    zscaler_hits = input("Enter the number of successful hits for each URL in Zscaler (separated by commas): ").split(',')
                    searches = input("Enter the searches performed for each URL (separated by commas): ").split(',')
                    summary = f"Phishing ({phishing_subtype})\n\n- URLs: {', '.join(urls)}\n\n- SWG Hits: {', '.join(swg_hits)}\n\n- Zeek Hits: {', '.join(zeek_hits)}\n\n- Zscaler Hits: {', '.join(zscaler_hits)}\n\n- Searches Performed: {', '.join(searches)}"
                else:
                    successful_deliveries = input("How many successful deliveries were there? ")
                    emails_blocked = input("How many emails got blocked? ")
                    summary = f"Phishing ({phishing_subtype})\n\n- Successful Deliveries: {successful_deliveries}\n\n- Emails Blocked: {emails_blocked}"
            elif case_type == "Network":
                operating_system_input = input("Enter the operating system: (1 for Windows, 2 for Mac, 3 for Linux): ")
                operating_system = get_operating_system(operating_system_input)
                root_cause = input("What was the root cause of the alert? ")
                rule = input("What was the rule of detection? ")
                summary = input("Write a technical summary: ")
                summary = f"Operating System: {operating_system}\n\n{summary}"
            elif case_type == "Host" or malicious.lower() == 'no':
                detection_type = input("Enter the type of detection: ")
                rule = input("What was the rule of detection? ")
                description = input("Write a description: ")
                root_cause = input("What was the root cause of the alert? ")
                summary = f"Detection Type: {detection_type}\n\n- Rule of Detection: {rule}\n\n- Description: {description}\n\nRoot Cause: {root_cause}"
            else:
                root_cause = input("What was the root cause of the alert? ")
                rule = input("What was the rule of detection? ")
                summary = input("Write a technical summary: ")
            actions = input("What actions did you take? ")

            save_to_file(file_path, malicious, case_type, root_cause, rule, actions, summary)

            go_back = input("Would you like to go back and change the case type? (yes/no): ")
            if go_back.lower() != 'yes':
                break
        else:
            print("No action required.")
            break

def get_case_type(case_type_input):
    if case_type_input == '1':
        return "Phishing"
    elif case_type_input == '2':
        return "Network"
    elif case_type_input == '3':
        return "Host"
    elif case_type_input == '4':
        return "Cloud"
    else:
        return "Other"

def get_phishing_subtype(phishing_subtype_input):
    if phishing_subtype_input == '1':
        return "Toad"
    elif phishing_subtype_input == '2':
        return "Credential Harvester"

def get_operating_system(operating_system_input):
    if operating_system_input == '1':
        return "Windows"
    elif operating_system_input == '2':
        return "Mac"
    elif operating_system_input == '3':
        return "Linux"

def save_to_file(file_path, malicious, case_type, root_cause, rule, actions, summary):
    with open(file_path, 'a') as file:
        file.write("Case Summary\n\n")
        file.write(f"Malicious: {malicious}\n\n")
        file.write(f"Case Type: {case_type}\n\n")
        file.write(f"Root Cause: {root_cause}\n\n")
        file.write(f"Rule of Detection: {rule}\n\n")
        file.write(f"Actions Taken: {actions}\n\n")
        file.write(f"Technical Summary:\n\n{summary}\n\n")
    print(f"Case summary saved to {file_path}")

if __name__ == "__main__":
    prompt_user()

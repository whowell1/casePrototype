import os

def main():
    case_number = input("Enter the case number: ")
    file_path = create_investigation_file(case_number)
    
    while True:
        case_type = select_case_type()
        summary = gather_case_details(case_type)
        actions = input("What actions did you take? ")
        
        save_to_file(file_path, case_type, summary, actions)

        go_back = input("Would you like to go back and change the case type? (yes/no): ")
        if go_back.lower() != 'yes':
            break

def create_investigation_file(case_number):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Investigations')
    os.makedirs(desktop_path, exist_ok=True)
    return os.path.join(desktop_path, f"{case_number}.md")

def select_case_type():
    case_types = {
        '1': 'Phishing',
        '2': 'Network',
        '3': 'Host',
        '4': 'Cloud',
        '5': 'Other'
    }
    while True:
        print("Select the type of case:")
        for key, value in case_types.items():
            print(f"{key}. {value}")
        choice = input("Enter the corresponding number: ")
        if choice in case_types:
            return case_types[choice]

def gather_case_details(case_type):
    if case_type == "Phishing":
        return gather_phishing_details()
    elif case_type == "Network":
        return gather_network_details()
    elif case_type == "Host":
        return gather_host_details()
    elif case_type == "Cloud":
        return gather_cloud_details()
    else:
        return gather_other_details()

def gather_phishing_details():
    email_from = input("Who was the email from? ")
    email_to = input("Who got the email? ")
    email_subject = input("What was the subject of the email? ")

    phishing_subtype = select_phishing_subtype()
    malicious = input("Was the email malicious? (yes/no): ")
    
    technical_summary = input("Write a technical summary: ")

    if malicious.lower() == 'yes':
        urls = input("Enter the list of URLs separated by commas: ").split(',')
        searches = input("Enter the searches performed for each URL (separated by commas): ").split(',')
        if phishing_subtype == 'Credential Harvester' or phishing_subtype == 'Toad':
            successful_deliveries = input("How many successful deliveries were there? ")
            emails_blocked = input("How many emails got blocked? ")
            summary = (
                f"Phishing ({phishing_subtype})\n\n"
                f"From: {email_from}\n\n"
                f"To: {email_to}\n\n"
                f"Subject: {email_subject}\n\n"
                f"Malicious: {malicious}\n\n"
                f"- URLs: {', '.join(urls)}\n\n"
                f"- Searches Performed: {', '.join(searches)}\n\n"
                f"- Successful Deliveries: {successful_deliveries}\n\n"
                f"- Emails Blocked: {emails_blocked}\n\n"
                f"Technical Summary: {technical_summary}"
            )
        else:
            summary = (
                f"Phishing ({phishing_subtype})\n\n"
                f"From: {email_from}\n\n"
                f"To: {email_to}\n\n"
                f"Subject: {email_subject}\n\n"
                f"Malicious: {malicious}\n\n"
                f"- URLs: {', '.join(urls)}\n\n"
                f"- Searches Performed: {', '.join(searches)}\n\n"
                f"Technical Summary: {technical_summary}"
            )
    else:
        false_positive_reason = input("Why is this a false positive? ")
        summary = (
            f"Phishing ({phishing_subtype})\n\n"
            f"From: {email_from}\n\n"
            f"To: {email_to}\n\n"
            f"Subject: {email_subject}\n\n"
            f"Malicious: {malicious}\n\n"
            f"Reason: {false_positive_reason}\n\n"
            f"Technical Summary: {technical_summary}"
        )

    return summary

def select_phishing_subtype():
    subtypes = {
        '1': 'Toad',
        '2': 'Credential Harvester'
    }
    while True:
        print("Was it a potential Toad or Credential Harvester? (1 for Toad, 2 for Credential Harvester): ")
        choice = input("Enter the corresponding number: ")
        if choice in subtypes:
            return subtypes[choice]

def gather_network_details():
    operating_system = select_operating_system()
    root_cause = input("What was the root cause of the alert? ")
    rule = input("What was the rule of detection? ")
    summary = input("Write a technical summary: ")
    return f"Operating System: {operating_system}\n\n{summary}"

def select_operating_system():
    operating_systems = {
        '1': 'Windows',
        '2': 'Mac',
        '3': 'Linux'
    }
    while True:
        print("Enter the operating system: (1 for Windows, 2 for Mac, 3 for Linux): ")
        choice = input("Enter the corresponding number: ")
        if choice in operating_systems:
            return operating_systems[choice]

def gather_host_details():
    detection_type = input("Enter the type of detection: ")
    rule = input("What was the rule of detection? ")
    description = input("Write a description: ")
    root_cause = input("What was the root cause of the alert? ")
    return f"Detection Type: {detection_type}\n\n- Rule of Detection: {rule}\n\n- Description: {description}\n\nRoot Cause: {root_cause}"

def gather_cloud_details():
    root_cause = input("What was the root cause of the alert? ")
    rule = input("What was the rule of detection? ")
    summary = input("Write a technical summary: ")
    return summary

def gather_other_details():
    root_cause = input("What was the root cause of the alert? ")
    rule = input("What was the rule of detection? ")
    summary = input("Write a technical summary: ")
    return summary

def save_to_file(file_path, case_type, summary, actions):
    with open(file_path, 'a') as file:
        file.write("# Case Summary\n\n")
        file.write(f"## Case Type: {case_type}\n\n")
        file.write(f"### Actions Taken: {actions}\n\n")
        file.write(f"### Technical Summary:\n\n{summary}\n\n")
    print(f"Case summary saved to {file_path}")

if __name__ == "__main__":
    main()

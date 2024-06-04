from email_scrapper.linkedin import LinkedIn

# Example usage:
if __name__ == "__main__":
    email = "abdullah.baig416@gmail.com"
    password = "Abdullaharfa48"

    linkedin = LinkedIn(email, password)
    linkedin.setup_driver()

    if linkedin.login():
        print("Login successful")

        # Example profile list for bulk scan
        # profiles = ["https://www.linkedin.com/in/profile1", "https://www.linkedin.com/in/profile2"]
        # emails = linkedin.bulk_scan(profiles)
        # print("Bulk scan emails:", emails)

        # Example profile for single scan
        single_profile = "https://www.linkedin.com/in/mujtaba-khalid-21b80a195"
        single_emails = linkedin.single_scan(single_profile)
        print("Single scan emails:", single_emails)
    else:
        print("Login failed")

    linkedin.quit_driver()

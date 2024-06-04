from email_scrapper.linkedin import LinkedIn as EmailLinkedIn
from search_scrapper.linkedin_scrapper import Linkedin as SearchLinkedIn
import xlsxwriter


def compile_data(search_data, email_data):
    for profile in search_data:
        profile_url = profile['profile_url']
        profile['email'] = email_data.get(profile_url, 'Not Available')

    # Write the compiled data to an Excel file
    workbook = xlsxwriter.Workbook("linkedin-compiled-data.xlsx")
    worksheet = workbook.add_worksheet('CompiledData')
    bold = workbook.add_format({'bold': True})
    worksheet.write(0, 0, 'Profile URL', bold)
    worksheet.write(0, 1, 'Name', bold)
    worksheet.write(0, 2, 'Connection Degree', bold)
    worksheet.write(0, 3, 'Location', bold)
    worksheet.write(0, 4, 'Title', bold)
    worksheet.write(0, 5, 'Email', bold)

    for i, profile in enumerate(search_data, start=1):
        worksheet.write(i, 0, profile['profile_url'])
        worksheet.write(i, 1, profile['name'])
        worksheet.write(i, 2, profile['connection_degree'])
        worksheet.write(i, 3, profile['location'])
        worksheet.write(i, 4, profile['title'])
        worksheet.write(i, 5, profile['email'])

    workbook.close()


# Example usage:
if __name__ == "__main__":
    email = "abdullah.baig416@gmail.com"
    password = "Abdullaharfa48"

    # Step 1: Run the search scraper
    search_linkedin = SearchLinkedIn(search_key="Backend developer", email=email, password=password, pages=2)
    search_linkedin.get_data()
    search_data = search_linkedin.data  # Collect the search data

    # Step 2: Extract profile URLs
    profile_urls = [profile['profile_url'] for profile in search_data if profile['profile_url']]

    # Step 3: Run the email scraper on the collected profile URLs
    email_linkedin = EmailLinkedIn(email, password)
    email_linkedin.setup_driver()

    if email_linkedin.login():
        print("Login successful")

        # Collect emails for all profiles
        email_data = {}
        for profile_url in profile_urls:
            emails = email_linkedin.single_scan(profile_url)
            email_data[profile_url] = emails[0] if emails else 'Not Available'

        email_linkedin.quit_driver()

        # Step 4: Compile the data
        compile_data(search_data, email_data)
        print("Data compiled successfully")
    else:
        print("Login failed")

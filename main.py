from scrapper.linkedin import LinkedInScraper
import xlsxwriter
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
search_query = os.getenv('SEARCH_QUERY')
pages = int(os.getenv('PAGES'))


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
    scraper = LinkedInScraper(email, password, search_query, pages)
    search_data, email_data = scraper.run()
    compile_data(search_data, email_data)
    print("Data compiled successfully")

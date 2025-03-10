import requests
import dotenv
import os
from canvasapi import Canvas

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
FILE_ID = os.getenv('FILE_ID')
COURSE_CODE = 89463

def check_existing_download():
    if os.path.exists(str(FILE_ID) + '.csv'):
        return True
    return False

def main():
    if not check_existing_download():
        canvas = Canvas('https://csulb.instructure.com', API_TOKEN)
        course = canvas.get_course(COURSE_CODE)
        file = course.get_file(FILE_ID)

        response = requests.get(file.url)
        with open(str(FILE_ID) + '.csv', 'wb') as f:
            f.write(response.content)

        print('File downloaded')
    else:
        print('File already downloaded')

if __name__ == '__main__':
    main();
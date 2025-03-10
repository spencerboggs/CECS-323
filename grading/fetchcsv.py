import requests
import dotenv
import os
from canvasapi import Canvas

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
COURSE_CODE = 89463
FILE_ID = 22161843

def main():
    canvas = Canvas('https://csulb.instructure.com', API_TOKEN)
    course = canvas.get_course(COURSE_CODE)
    file = course.get_file(FILE_ID)

    response = requests.get(file.url)
    with open('data.csv', 'wb') as f:
        f.write(response.content)

    print('File downloaded')

if __name__ == '__main__':
    main();
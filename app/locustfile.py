import requests

from locust import HttpUser, task

API_PATH = 'https://stolarski.bieda.it/api/v1'


class HelloWorldUser(HttpUser):

    auth_response = requests.post(
            url=API_PATH+'/auth/token',
            data={'username': 'admin', 'password': 'admin'})
    client_headers = {
            'Authorization': "Bearer " + auth_response.json()['access_token']}

    @task
    def prime(self):
        self.client.get(f"/prime/21312412")
    
    @task
    def img_invert(self):
        self.client.post(
            "/picture/invert/",
            files=[
                ('file', (
                    'img2.jpg',open(
                        'C:/Users/Szymon.Stolarski/Desktop/img2.jpg','rb'),
                    'image/jpeg'))]
        )

    @task
    def get_time(self):
        self.client.get('/time/get',
                        headers=HelloWorldUser.client_headers)
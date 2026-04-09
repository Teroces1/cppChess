import requests

class Life360API:
    def __init__(self, username, password):
        self.base_url = "https://www.life360.com/v3"
        self.session = requests.Session()
        
        # Authenticate immediately upon creating the object
        self._authenticate(username, password)

    def _authenticate(self, username, password):
        """Logs in and gets the Bearer token."""
        auth_url = f"{self.base_url}/oauth2/token.json"
        
        # This is the hardcoded Basic Auth token used by the Life360 Android app
        client_auth = "cFJFcXVlc3RBcHBBbmRyb2lkOllFcXVlc3RBcHBBbmRyb2lk"
        
        headers = {
            "Authorization": f"Basic {client_auth}",
            "Accept": "application/json"
        }
        
        payload = {
            "grant_type": "password",
            "username": username,
            "password": password
        }
        
        response = self.session.post(auth_url, headers=headers, data=payload)
        response.raise_for_status() # Raise an error if login fails
        
        # Extract the access token
        access_token = response.json().get("access_token")
        
        # Update the session headers so all future requests use this Bearer token
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        })
        print("Successfully authenticated with Life360!")

    # ==========================================
    # ENDPOINTS
    # ==========================================

    def get_user_me(self):
        """Get authenticated user profile."""
        response = self.session.get(f"{self.base_url}/users/me")
        return response.json()

    def get_circles(self):
        """Get all Circles you belong to."""
        response = self.session.get(f"{self.base_url}/circles")
        return response.json()

    def get_circle(self, circle_id):
        """Get detailed Circle info including members."""
        response = self.session.get(f"{self.base_url}/circles/{circle_id}")
        return response.json()

    def get_circle_members(self, circle_id):
        """Get Members in a Circle."""
        response = self.session.get(f"{self.base_url}/circles/{circle_id}/members")
        return response.json()

    def get_member(self, circle_id, member_id):
        """Get specific Member details (including location)."""
        response = self.session.get(f"{self.base_url}/circles/{circle_id}/members/{member_id}")
        return response.json()

    def get_circle_places(self, circle_id):
        """Get Places for a Circle."""
        response = self.session.get(f"{self.base_url}/circles/{circle_id}/places")
        return response.json()

    def get_place(self, circle_id, place_id):
        """Get detailed Place info."""
        response = self.session.get(f"{self.base_url}/circles/{circle_id}/places/{place_id}")
        return response.json()

# ==========================================
# EXAMPLE USAGE
# ==========================================
if __name__ == "__main__":
    # 1. Initialize and login
    USERNAME = "your_email@example.com"
    PASSWORD = "your_password"
    
    try:
        api = Life360API(USERNAME, PASSWORD)
        
        # 2. Get your circles
        circles_data = api.get_circles()
        
        # 3. Get the ID of the first circle
        first_circle_id = circles_data['circles'][0]['id']
        first_circle_name = circles_data['circles'][0]['name']
        print(f"\nFetching data for Circle: {first_circle_name} ({first_circle_id})")
        
        # 4. Get members of that circle
        members_data = api.get_circle_members(first_circle_id)
        
        # 5. Print out member names and their battery life/location
        for member in members_data['members']:
            name = member['firstName']
            battery = member['location']['battery']
            address = member['location']['name'] or member['location']['address1']
            
            print(f"- {name}: {battery}% battery, currently at {address}")
            
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
import time
import unittest
from selenium import webdriver
from django.contrib.auth.models import User

from selenium.webdriver.common.by import By

# Login Credentials for testing purpose only.
username = "test"
password = "test"


class TodoAppE2ETest(unittest.TestCase):

    def setUp(self):
        """Initialise Webdriver"""
        options = webdriver.ChromeOptions()  # Driver Setting for a headless Webdriver
        options.add_argument("--headless")  # Run in Headless mode
        # options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # Disable the Shared Memory

        self.driver = webdriver.Chrome(options=options)  # Initialisation

    def test_new_user_register(self):
        """Test the Registration of New User"""

        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/register/")  # Registration URL

        # Find the username box and send in the username
        username = driver.find_element(By.NAME, "username")
        username.send_keys("testuser")

        # Find the password box and send in the password
        password = driver.find_element(By.NAME, "password")
        password.send_keys("testpass")

        # Finding the Form Action
        form_action = driver.find_element(By.CLASS_NAME, "form-actions")

        # Finding the POST button to feed the user to the db
        post_button = form_action.find_element(
            By.CLASS_NAME, "btn.btn-primary.js-tooltip"
        )
        post_button.click()

        time.sleep(2)
        # Verify the creation of new user
        self.assertIn("201", driver.page_source)
        print("New User is CREATED!")

        # Deleting the Test User created from the DB
        user = User.objects.filter(username="testuser")
        user.delete()
        driver.close()

    def test_login(self):
        """Test user login with Basic Authentication"""
        driver = self.driver
        driver.get("http://127.0.0.1:8000/api/todo/")

        # Use Basic Authentication (Sending credentials in URL)
        driver.get(f"http://{username}:{password}@127.0.0.1:8000/api/todo/")

        time.sleep(2)

        # Check if login was successfull by looking for some expected Text
        self.assertIn("Todo List Create", driver.page_source)
        print("Succesful LOGIN!")
        driver.close()

    def test_create_task(self):
        """Test to add a New To-Do task"""

        driver = self.driver
        driver.get(f"http://{username}:{password}@localhost:8000/api/todo/")

        # Find the "Title" box and fill it with title of the task
        title_box = driver.find_element(By.NAME, "title")
        title_box.send_keys("Title Testing")

        # Finding the "Description" Box and sending some description
        desc_box = driver.find_element(By.NAME, "description")
        desc_box.send_keys("Description Testing")

        time.sleep(1)

        # Finding the Form Action
        form_action = driver.find_element(By.CLASS_NAME, "form-actions")

        # Finding the POST button to feed the task to the to-do list
        post_button = form_action.find_element(
            By.CLASS_NAME, "btn.btn-primary.js-tooltip"
        )
        post_button.click()

        time.sleep(2)  # Wait for updatation

        # Verify Task appears in the list
        self.assertIn("Title Testing", driver.page_source)
        print("New Task is CREATED!")
        driver.close()

    def test_view_task_list(self):
        """Test to the view the List of To-Do for that User"""

        driver = self.driver
        driver.get(f"http://{username}:{password}@localhost:8000/api/todo/")

        time.sleep(2)

        # Verify that at least 1 task is present
        self.assertIn("timestamp", driver.page_source, "No To-do found!")
        print("All the Task for the user are LISTED!")
        driver.close()

    def test_update_and_delete_task(self):
        """Test updating a To-do"""

        driver = self.driver
        driver.get(f"http://{username}:{password}@localhost:8000/api/todo/")

        # Finding the tasks id to update
        task_id = driver.find_elements(By.CLASS_NAME, "lit")

        try:
            task_id = int(
                task_id[3].text
            )  # Fetching the ID of the first task to update
            print(task_id)          # and converting it to integer
        except IndexError:
            print("No task present to update")
            return

        # Visiting the Task with the task_id to perform updation and deletion
        driver.get(f"http://{username}:{password}@localhost:8000/api/todo/{task_id}")

        # Finding the title box and fill it with title of the task
        title_box = driver.find_element(By.NAME, "title")
        title_box.clear()
        title_box.send_keys("Updated Title Testing")

        due_date_box = driver.find_element(By.NAME, "due_date")
        due_date_box.clear()

        # Finding the Description Box and sending some description
        desc_box = driver.find_element(By.NAME, "description")
        desc_box.clear()
        desc_box.send_keys("Updated Description Testing")

        # Finding the Form Action
        form_action = driver.find_element(By.CLASS_NAME, "form-actions")

        # Finding the PUT button to feed the task to the to-do list
        put_button = form_action.find_element(
            By.CLASS_NAME, "btn.btn-primary.js-tooltip"
        )
        put_button.click()

        time.sleep(5)  # Wait for Updation

        # Verify update
        self.assertIn("Updated Title Testing", driver.page_source)
        print(f"Task with the id:{task_id} is UPDATED!")

        # Deleting the record with the fetched task_id

        time.sleep(3)

        # Finding the Delete button and clicking it
        delete_btn = driver.find_element(
            By.CLASS_NAME, "btn.btn-danger.button-form.js-tooltip"
        )
        delete_btn.click()
        time.sleep(3)

        # Finding the delete button in the alert box(for confirmation)
        # and clicking it to delete the task
        delete_form_btn = driver.find_element(
            By.XPATH,
            """//div[@class='modal-footer']
            //form[@class='button-form']
            //button[@class='btn btn-danger']""",
        )
        # print(delete_form_btn.text)
        delete_form_btn.click()

        time.sleep(7)
        # Verifying the deletion of the task
        self.assertIn("204 No Content", driver.page_source)
        print(f"Task with the id:{task_id} is DELETED!")
        driver.close()

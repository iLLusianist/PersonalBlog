import unittest
from flask_testing import TestCase
from app import app
from parameterized import parameterized


class AppTest(TestCase):
    @staticmethod
    def create_app():
        app.config['TESTING'] = True
        return app

    # @parameterized.expand([
    #     ('1234', '1234')
    # ])
    # def test_registration_successful(self, login, password):
    #     print('\n\nTest "test_registration_successful"')
    #     with self.client as client:
    #         response = client.post(
    #             '/registration',
    #             data = {
    #                 'sign_up_login': login,
    #                 'sign_up_password': password,
    #                 'sign_up_repeat_password': password,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects = True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTemplateUsed('sign_in.html')
    #
    # @parameterized.expand([
    #     ('iLLusi', '123')
    # ])
    # def test_registration_failed_duplicate_login(self, login, password):
    #     print('\n\nTest "test_registration_failed_duplicate_login"')
    #     with self.client as client:
    #         client.post(
    #             '/registration',
    #             data = {
    #                 'sign_up_login': login,
    #                 'sign_up_password': password,
    #                 'sign_up_repeat_password': password,
    #                 'is_test': True
    #             },
    #             follow_redirects = True
    #         )
    #
    #         response = client.post(
    #             '/registration',
    #             data = {
    #                 'sign_up_login': login,
    #                 'sign_up_password': password,
    #                 'sign_up_repeat_password': password,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects=True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'already taken")</script>', response.data)
    #         self.assertTemplateUsed('sign_up.html')
    #
    # @parameterized.expand([
    #     ('iLLusi', '123', '124')
    # ])
    # def test_registration_failed_passwords_not_match(self, login, password, repeat_password):
    #     print('\n\nTest "test_registration_failed_passwords_not_match"')
    #     with self.client as client:
    #         response = client.post(
    #             '/registration',
    #             data={
    #                 'sign_up_login': login,
    #                 'sign_up_password': password,
    #                 'sign_up_repeat_password': repeat_password,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects=True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'<script>alert("Passwords do not match")</script>', response.data)
    #         self.assertTemplateUsed('sign_up.html')
    #
    # @parameterized.expand([
    #     ('iLLusi', '123')
    # ])
    # def test_authorization_successful_username_found(self, login, password):
    #     print('\n\nTest "test_authorization_successful_username_found"')
    #     with self.client as client:
    #         client.post(
    #             '/registration',
    #             data = {
    #                 'sign_up_login': login,
    #                 'sign_up_password': password,
    #                 'sign_up_repeat_password': password,
    #                 'is_test': True
    #             },
    #             follow_redirects = True
    #         )
    #         response = client.post(
    #             '/authorization',
    #             data = {
    #                 'sign_in_login': login,
    #                 'sign_in_password': password,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects = True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTemplateUsed('index.html')
    #
    # @parameterized.expand([
    #     ('iLLusi', '123')
    # ])
    # def test_authorization_failed_username_not_found(self, login, password):
    #     print('\n\nTest "test_authorization_failed_username_not_found"')
    #     with self.client as client:
    #         response = client.post(
    #             '/authorization',
    #             data = {
    #                 'sign_in_login': login,
    #                 'sign_in_password': password,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects = True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'not found")</script>', response.data)
    #         self.assertTemplateUsed('sign_in.html')
    #
    # @parameterized.expand([
    #     ('iLLusi', '123', '124')
    # ])
    # def test_authorization_failed_password_do_not_match(self, login, password, database_password):
    #     print('\n\nTest "test_authorization_failed_password_do_not_match"')
    #     with self.client as client:
    #         client.post(
    #             '/registration',
    #             data = {
    #                 'sign_up_login': login,
    #                 'sign_up_password': password,
    #                 'sign_up_repeat_password': password,
    #                 'is_test': True
    #             },
    #             follow_redirects=True
    #         )
    #         response = client.post(
    #             '/authorization',
    #             data = {
    #                 'sign_in_login': login,
    #                 'sign_in_password': database_password,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects=True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'<script>alert("Passwords do not match")</script>', response.data)
    #         self.assertTemplateUsed('sign_in.html')
    #
    # @parameterized.expand([
    #     ('1234', '1234')
    # ])
    # def test_add_successful_add_blog(self, title, text):
    #     print('\n\nTest "test_add_successful_add_blog"')
    #     with self.client as client:
    #         response = client.post(
    #             '/write_blog',
    #             data = {
    #                 'add_title': title,
    #                 'add_text': text,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects = True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTemplateUsed('index.html')
    #
    # @parameterized.expand([
    #     ('123', ''),
    #     ('', '123'),
    #     ('', '')
    # ])
    # def test_add_failed_value_is_empty(self, title, text):
    #     print('\n\nTest "test_add_failed_value_is_empty"')
    #     with self.client as client:
    #         response = client.post(
    #             '/write_blog',
    #             data = {
    #                 'add_title': title,
    #                 'add_text': text,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects = True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'<script>alert("Title or text is empty")</script>', response.data)
    #         self.assertTemplateUsed('add.html')
    #
    # @parameterized.expand([
    #     ('1234', '1234')
    # ])
    # def test_add_failed_duplicate_blog(self, title, text):
    #     print('\n\nTest "test_add_successful_add_blog"')
    #     with self.client as client:
    #         client.post(
    #             '/write_blog',
    #             data = {
    #                 'add_title': title,
    #                 'add_text': text,
    #                 'is_test': True,
    #             },
    #         )
    #
    #         response = client.post(
    #             '/write_blog',
    #             data = {
    #                 'add_title': title,
    #                 'add_text': text,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #             follow_redirects = True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTemplateUsed('add.html')
    #         self.assertIn(b'already exists")</script>', response.data)

    @parameterized.expand([
        ('Login', 'Password', 'Title1', 'Title2', 'Title3', 'Text1', 'Text2')
    ])
    def test_edit_successful_edit_blog(self, login, password, title1, title2, title3, text1, text2):
        print('\n\nTest "test_edit_successful_edit_blog"')
        with self.client as client:
            client.post(
                '/registration',
                data={
                    'sign_up_login': login,
                    'sign_up_password': password,
                    'sign_up_repeat_password': password,
                    'is_test': True,
                },
            )

            client.post(
                '/authorization',
                data={
                    'sign_in_login': login,
                    'sign_in_password': password,
                    'is_test': True,
                    'test_ended': True
                },
            )

            client.post(
                '/write_blog',
                data={
                    'add_title': title1,
                    'add_text': text1,
                    'is_test': True,
                },
            )

            client.post(
                '/write_blog',
                data={
                    'add_title': title2,
                    'add_text': text2,
                    'is_test': True,
                },
            )

            response = client.post(
                '/edit_blog',
                query_string = {
                    'title': title1
                },
                data = {
                    'edit_title': title3,
                    'edit_text': text2,
                    'is_test': True,
                    'test_ended': True,
                },
                follow_redirects = True
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('index.html')

    # @parameterized.expand([
    #     ('Login', 'Password', 'Title1', 'Title2', 'Text1', 'Text2')
    # ])
    # def test_edit_failed_duplicate_blog(self, login, password, title1, title2, text1, text2):
    #     print('\n\nTest "test_edit_failed_duplicate_blog"')
    #     with self.client as client:
    #         client.post(
    #             '/registration',
    #             data={
    #                 'sign_up_login': login,
    #                 'sign_up_password': password,
    #                 'sign_up_repeat_password': password,
    #                 'is_test': True,
    #             },
    #         )
    #
    #         client.post(
    #             '/authorization',
    #             data={
    #                 'sign_in_login': login,
    #                 'sign_in_password': password,
    #                 'is_test': True,
    #                 'test_ended': True
    #             },
    #         )
    #
    #         client.post(
    #             '/write_blog',
    #             data={
    #                 'add_title': title1,
    #                 'add_text': text1,
    #                 'is_test': True,
    #             },
    #         )
    #
    #         client.post(
    #             '/write_blog',
    #             data={
    #                 'add_title': title2,
    #                 'add_text': text2,
    #                 'is_test': True,
    #             },
    #         )
    #
    #         response = client.post(
    #             '/edit_blog',
    #             query_string = {
    #                 'title': title1
    #             },
    #             data = {
    #                 'edit_title': title2,
    #                 'edit_text': text2,
    #                 'is_test': True,
    #                 'test_ended': True,
    #             },
    #             follow_redirects = True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTemplateUsed('edit.html')




if __name__ == '__main__':
    unittest.main()
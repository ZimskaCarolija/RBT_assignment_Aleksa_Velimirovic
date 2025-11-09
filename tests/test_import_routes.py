import pytest
import json
from io import BytesIO


class TestImportRoutes:

    def create_csv_file(self, content: str, filename: str = 'test.csv'):
        file_content = BytesIO()
        file_content.write(content.encode('utf-8'))
        file_content.seek(0)
        return (file_content, filename)

    # /import/users - success
    def test_import_users_success(self, client, admin_auth_headers, employee_role):
        csv_content = """Vacation year,2019
        Employee Email,Employee Password
        user1@rbt.rs,Abc!@#$
        user2@rbt.rs,Abc!@#$
        user3@rbt.rs,Abc!@#$"""
        csv_file = self.create_csv_file(csv_content, 'users.csv')
        
        response = client.post(
            '/import/users',
            data={'file': csv_file},
            content_type='multipart/form-data',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # /import/users - fail
    def test_import_users_unauthorized(self, client, employee_auth_headers, employee_role):
        csv_content = """Vacation year,2019
        Employee Email,Employee Password
        user1@rbt.rs,Abc!@#$"""
        csv_file = self.create_csv_file(csv_content, 'users.csv')
        
        response = client.post(
            '/import/users',
            data={'file': csv_file},
            content_type='multipart/form-data',
            headers=employee_auth_headers
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False

    # /import/vacations - success
    def test_import_vacations_success(self, client, admin_auth_headers, employee_user, vacation_entitlement):
        csv_content = """Employee,Vacation start date,Vacation end date
        employee@test.com,"Friday, August 30, 2019","Wednesday, September 11, 2019"
        employee@test.com,"Thursday, October 24, 2019","Thursday, October 24, 2019"
        employee@test.com,"Friday, November 22, 2019","Friday, November 22, 2019"
        employee@test.com,"Monday, March 9, 2020","Monday, March 9, 2020"
        employee@test.com,"Monday, May 25, 2020","Thursday, May 28, 2020\""""
        csv_file = self.create_csv_file(csv_content, 'vacations.csv')
        
        response = client.post(
            '/import/vacations',
            data={'file': csv_file},
            content_type='multipart/form-data',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # /import/vacations - fail
    def test_import_vacations_missing_file(self, client, admin_auth_headers):
        response = client.post(
            '/import/vacations',
            content_type='multipart/form-data',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # /import/entitlements - success
    def test_import_entitlements_success(self, client, admin_auth_headers, employee_user):
        csv_content = """Vacation year,2019
        Employee,Total vacation days
        employee@test.com,20"""
        csv_file = self.create_csv_file(csv_content, 'entitlements.csv')
        
        response = client.post(
            '/import/entitlements',
            data={'file': csv_file},
            content_type='multipart/form-data',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # /import/entitlements - fail
    def test_import_entitlements_unauthorized(self, client, employee_auth_headers, employee_user):
        csv_content = """Vacation year,2019
        Employee,Total vacation days
        employee@test.com,20"""
        csv_file = self.create_csv_file(csv_content, 'entitlements.csv')
        
        response = client.post(
            '/import/entitlements',
            data={'file': csv_file},
            content_type='multipart/form-data',
            headers=employee_auth_headers
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False

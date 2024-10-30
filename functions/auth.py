import os
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer


azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=os.environ.get("APP_CLIENT_ID"),
    tenant_id=os.environ.get("TENANT_ID"),
    scopes={os.environ.get('APP_ID_URI'):os.environ.get('SCOPE_NAME')},
    allow_guest_users=True
)

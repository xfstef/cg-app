from pydantic import BaseSettings


class Settings(BaseSettings):
   # Base
   api_v1_prefix: str
   debug: bool
   project_name: str
   version: str
   description: str

   # Database
   db_async_connection_str: str

   # [Security]
   auth_algorithm: str
   auth_token_expire: int
   auth_secret_key: str
   email_secret_key: str
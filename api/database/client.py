import os
from dotenv import load_dotenv
from supabase import create_client

class SupabaseClient:
    def __init__(self):
        load_dotenv()
        SUPABASE_URL = os.environ.get("SUPABASE_URL")
        SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
        self.client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
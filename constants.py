import os
import dotenv


# Load the environment variables
dotenv.load_dotenv()

OPENAPI_KEY = os.getenv("OPENAI_API_KEY")
METAPHOR_KEY = os.getenv("METAPHOR_API_KEY")

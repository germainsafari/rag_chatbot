

```markdown
### Chatbot Application

This is a chatbot application that integrates RAG with OpenAI's GPT-4 model on custom data, built using Streamlit. Follow the instructions below to set up and run the application on your local machine.

## Prerequisites

Ensure you have the following installed:

- Python (preferably Python 3.7 or higher)
- Pip (Python's package installer)
- Streamlit

## Setup

### 1. Create a Virtual Environment

First, navigate to the project directory and create a virtual environment:

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

Activate the virtual environment by running the appropriate command:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Set Up Your Environment Variables

Create a `.env` file in the root directory of your project and add your `OPENAI_API_KEY`:

```ini
OPENAI_API_KEY=***
```

Alternatively, you can set the environment variable using `set`:

- On Windows:

```bash
set OPENAI_API_KEY=***
```

- On macOS/Linux:

```bash
export OPENAI_API_KEY=***
```

### 5. Run the Application

Navigate to the `chatbot` directory:

```bash
cd chatbot
```

Run the Streamlit application:

```bash
streamlit run main.py
```

This will start the chatbot on your local server, and you can access it via the browser.

---

Happy chatting!
```

Let me know if you need any adjustments or additional details!

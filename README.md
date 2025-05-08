# 🎓 College Agent - AI Assistant powered by Google ADK

A smart AI assistant for college information, built using Google's Agent Development Kit (ADK), FastAPI, and Vertex AI RAG for knowledge retrieval.

## 📋 Overview

College Agent is an AI-powered chatbot designed to answer questions about college information using a corpus of documents. The agent leverages Google's Generative AI capabilities through the Agent Development Kit (ADK) and Retrieval-Augmented Generation (RAG) to provide accurate, contextual responses based on the college's documentation.

## 🔍 Key Features

- **RAG-powered Knowledge Base**: Uses Vertex AI RAG to retrieve information from a corpus of college documents
- **FastAPI Integration**: Provides a robust API for frontend integration
- **Containerized Deployment**: Ready for deployment on Google Cloud Run
- **Streaming Responses**: Supports Server-Sent Events (SSE) for real-time streaming responses
- **Session Management**: Maintains user session state for personalized interactions

## 🛠️ Project Structure

```
college-agent/
├── college_agent/           # ADK agent directory
│   ├── __init__.py          # Contains: from . import agent
│   ├── agent.py             # Defines the root_agent
│   ├── prompts.py           # Contains agent instructions
│   └── shared_libraries/    # Utility modules
│       └── corpus.py        # RAG corpus management
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
├── .env                     # Environment variables
└── sessions.db              # Local SQLite for session state
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Google Cloud account with Vertex AI access
- Google Cloud CLI installed (for deployment)

### Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd college-agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_GENAI_USE_VERTEXAI=True
   RAG_CORPUS=projects/your-project-number/locations/us-central1/ragCorpora/your-corpus-id
   ```

## 📚 Corpus Management

### Creating and Uploading to RAG Corpus

The project includes a utility script (`corpus.py`) to create and manage the RAG corpus:

1. **Prepare your PDF document** according to the guidelines below
2. **Configure the PDF location**:
   - The script expects a PDF named `ssragcorpus.pdf`
   - Default location: `D:\college_Agent\college_agent\shared_libraries\ssragcorpus.pdf`
   - To use a different file or location, modify these variables in `corpus.py`:
     ```python
     PDF_FILENAME = "ssragcorpus.pdf"
     LOCAL_PDF_PATH = "D:\\college_Agent\\college_agent\\shared_libraries\\ssragcorpus.pdf"
     ```
3. **Run the corpus management script**:
   ```bash
   python -m college_agent.shared_libraries.corpus
   ```
4. The script will:
   - Create a new corpus or use an existing one with the name "SSRagCorpus"
   - Upload your PDF to the corpus
   - Update your `.env` file with the RAG_CORPUS ID

### Corpus Document Guidelines

For optimal chatbot performance, follow these guidelines when creating documents:

1. **Use a Simple Format**:
   - Save documents as PDFs or plain text (.txt)
   - Avoid complex formatting that might confuse the RAG system

2. **Organize Information**:
   - *Separate by Topic*: Create different files for each topic (e.g., "Admissions", "Campus Facilities")
   - *Use Clear Headings*: Add headings like "# Admissions" or "## How to Apply"
   - *Write Short Paragraphs*: Keep paragraphs to 2-3 sentences
   - *Use Lists*: For steps or options, use bullets or numbers

3. **Write Clearly**:
   - Use simple words as if explaining to a student
   - Be specific rather than general (e.g., list actual courses instead of saying "many courses")
   - Include answers to common questions
   - Avoid unexplained abbreviations

4. **Maintain Consistency**:
   - Use consistent terminology throughout documents
   - Add the year for time-sensitive information (e.g., "Admissions 2025")
   - Check for spelling and grammar mistakes

5. **Test Your Documents**:
   - Ensure comprehensive coverage of topics users might ask about
   - Work with the chatbot team to verify the chatbot finds correct answers

### Sample Document Format

```markdown
# Admissions 2025
## Who Can Apply
- Students with 50% or more in 12th grade.
- Some courses need an entrance exam.

## How to Apply
1. Go to www.collegewebsite.edu.
2. Fill out the application form.
3. Upload your 12th-grade marks and ID.
4. Pay the $50 fee.
5. Submit by June 30, 2025.
```

## 🖥️ Local Development

Run the application locally:

```bash
python main.py
```

The server will start at http://localhost:8080 with a web interface for testing.

## ☁️ Deployment to Google Cloud Run

1. Set environment variables:
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   export GOOGLE_CLOUD_LOCATION=us-central1
   export GOOGLE_GENAI_USE_VERTEXAI=True
   export RAG_CORPUS=projects/your-project-number/locations/us-central1/ragCorpora/your-corpus-id
   ```

2. Authenticate with Google Cloud:
   ```bash
   gcloud auth login
   gcloud config set project $GOOGLE_CLOUD_PROJECT
   ```

3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy college-agent \
     --source . \
     --region $GOOGLE_CLOUD_LOCATION \
     --project $GOOGLE_CLOUD_PROJECT \
     --allow-unauthenticated \
     --set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI,RAG_CORPUS=$RAG_CORPUS"
   ```

## 🌐 API Integration Guide

### Base URL

```
https://college-agent-service-320796335529.us-central1.run.app
```

### API Endpoints

#### 1. Create or Update a Session

```
POST /apps/{app_name}/users/{user_id}/sessions/{session_id}
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "state": {
    "preferred_language": "English",
    "visit_count": 1
  }
}
```

#### 2. Send a Message (with Streaming Support)

```
POST /run_sse
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "app_name": "college_agent",
  "user_id": "user_123",
  "session_id": "session_abc",
  "new_message": {
    "role": "user",
    "parts": [{
      "text": "What are the admission requirements?"
    }]
  },
  "streaming": true
}
```

### Example Frontend Integration

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>College Agent Chat</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 2rem;
      background: #f5f5f5;
    }
    .container {
      max-width: 600px;
      margin: auto;
      background: white;
      padding: 2rem;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    input, textarea, button {
      width: 100%;
      padding: 0.8rem;
      margin-bottom: 1rem;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    #response {
      white-space: pre-wrap;
      background: #eee;
      padding: 1rem;
      border-radius: 5px;
      height: 150px;
      overflow-y: auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>🎓 College Agent Chat</h2>

    <input type="text" id="userId" placeholder="Enter User ID" value="user_123" />
    <input type="text" id="sessionId" placeholder="Enter Session ID" value="session_abc" />
    <textarea id="messageInput" placeholder="Type your message here...">Hi there!</textarea>

    <button onclick="startChat()">Send Message</button>

    <h3>Response:</h3>
    <div id="response"></div>
  </div>

  <script>
    const BASE_URL = "https://college-agent-service-320796335529.us-central1.run.app";

    async function startChat() {
      const userId = document.getElementById("userId").value;
      const sessionId = document.getElementById("sessionId").value;
      const messageText = document.getElementById("messageInput").value;
      const responseDiv = document.getElementById("response");
      responseDiv.innerText = "Starting...\n";

      // Step 1: Initialize session
      const sessionUrl = `${BASE_URL}/apps/college_agent/users/${userId}/sessions/${sessionId}`;
      const sessionState = {
        state: {
          preferred_language: "English",
          visit_count: 1
        }
      };

      try {
        const initRes = await fetch(sessionUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(sessionState)
        });

        if (!initRes.ok) {
          const err = await initRes.json();
          responseDiv.innerText += `Session Error: ${JSON.stringify(err)}\n`;
          return;
        }

        responseDiv.innerText += "Session initialized.\n";

        // Step 2: Call run_sse endpoint using fetch stream
        const sseUrl = `${BASE_URL}/run_sse`;

        const res = await fetch(sseUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            app_name: "college_agent",
            user_id: userId,
            session_id: sessionId,
            new_message: {
              role: "user",
              parts: [{ text: messageText }]
            },
            streaming: true
          })
        });

        const reader = res.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value);
          responseDiv.innerText += chunk;
          responseDiv.scrollTop = responseDiv.scrollHeight;
        }

      } catch (err) {
        console.error(err);
        responseDiv.innerText += `\n❌ Error: ${err.message}`;
      }
    }
  </script>
</body>
</html>
```


## 🙏 Acknowledgements

- Google Agent Development Kit (ADK)
- Vertex AI and Generative AI technologies
- FastAPI framework

# AI Debate: Mistral vs DeepSeek

A Python application that creates an engaging conversation between two AI models with contrasting personalities: an argumentative Mistral and a polite DeepSeek. The conversation is automatically saved in markdown format with visible thought processes.

## Features

- **Two Distinct AI Personalities:**

  - 🔥 **Mistral**: An argumentative and snarky chatbot that challenges everything
  - 🤝 **DeepSeek**: A polite and courteous chatbot that seeks common ground

- **Rich Markdown Formatting:**

  - Visible thought processes in collapsible sections
  - Bold and italic text for emphasis
  - Blockquotes and lists for better structure
  - Timestamps for each message

- **Real-time Conversation:**
  - Automatic saving after each turn
  - Beautiful markdown output
  - Expandable thought process sections

## Prerequisites

- Python 3.11 or higher
- UV package manager
- API keys for both Mistral and Groq

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MuhammadRaffey/AI-Debate.git
cd AI-Debate
```

2. Install dependencies using UV:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

3. Create a `.env` file in the project root with your API keys:

```env
MISTRAL_API_KEY=your_mistral_api_key
GROQ_API_KEY=your_groq_api_key
```

## Usage

1. Run the conversation:

```bash
uv run demo
```

2. The conversation will be saved in `chat.md` in the project root directory.

3. View the conversation:
   - Open `chat.md` in any markdown viewer
   - Each turn includes:
     - Timestamp
     - Message content
     - Thought process (for DeepSeek)
     - Formatting for better readability

## Output Format

The conversation is saved in a structured markdown format:

```markdown
# Conversation between Mistral and DeepSeek

> This is an AI conversation between two models with different personalities:
>
> - Mistral: An argumentative and snarky chatbot
> - DeepSeek: A polite and courteous chatbot that shows its thought process

## Conversation

### Turn 1 - Mistral (timestamp)

[Mistral's message]

### Turn 1 - DeepSeek (timestamp)

<details>
<summary>🤔 Thought Process</summary>

> **Analysis:** > [DeepSeek's thought process]

</details>

### Response:

[DeepSeek's response]
```

## Configuration

You can modify the following parameters in `main.py`:

- `mistral_model`: The Mistral model to use
- `groq_model`: The DeepSeek model to use via Groq
- `mistral_system`: The system prompt for Mistral's personality
- `groq_system`: The system prompt for DeepSeek's personality

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

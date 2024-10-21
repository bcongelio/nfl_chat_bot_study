document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // Function to add a message to the chat
    function addMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        
        // Check if the message contains code blocks
        const parts = message.split(/(```[\s\S]*?```)/);
        parts.forEach(part => {
            if (part.startsWith('```') && part.endsWith('```')) {
                // This is a code block
                const codeElement = document.createElement('pre');
                const codeContent = part.slice(3, -3).trim(); // Remove ``` from start and end
                
                codeElement.innerHTML = `<code class="language-r">${escapeHtml(codeContent)}</code>`;
                messageElement.appendChild(codeElement);
            } else {
                // This is regular text
                const textNode = document.createTextNode(part);
                messageElement.appendChild(textNode);
            }
        });
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Highlight code blocks
        Prism.highlightAllUnder(messageElement);
    }

    // Escape HTML to prevent XSS
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Handle form submission
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message) {
            addMessage('user', `You said: ${message}`);
            userInput.value = '';

            setTimeout(() => {
                const botResponse = getBotResponse(message);
                addMessage('bot', botResponse);
            }, 1000);
        }
    });

    // Simple bot response function with R code examples
    function getBotResponse(message) {
        const responses = [
            "Here's an example of a tidy R function:\n```\nlibrary(dplyr)\n\nclean_data <- function(df) {\n  df %>%\n    filter(!is.na(value)) %>%\n    group_by(category) %>%\n    summarize(mean_value = mean(value))\n}\n```\nThis function cleans a dataframe by removing NA values and calculating mean values per category.",
            "Let's look at a ggplot2 example:\n```\nlibrary(ggplot2)\n\nggplot(mtcars, aes(x = mpg, y = wt)) +\n  geom_point() +\n  geom_smooth(method = 'lm') +\n  labs(title = 'MPG vs Weight',\n       x = 'Miles per Gallon',\n       y = 'Weight (1000 lbs)')\n```\nThis code creates a scatter plot with a linear regression line.",
            "Here's how you might use purrr for functional programming:\n```\nlibrary(purrr)\n\nnumbers <- list(1:5, 6:10, 11:15)\nmap_dbl(numbers, mean)\n```\nThis code calculates the mean of each sublist using `map_dbl()`."
        ];
        return responses[Math.floor(Math.random() * responses.length)];
    }
});

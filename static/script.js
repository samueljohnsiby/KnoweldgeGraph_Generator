function submitQuestion() {
    const userInput = document.getElementById('user-input').value;

    // Add user's question to the chat window
    appendUserQuestion(userInput);

    const requestData = { question: userInput };

    fetch('/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response from Flask
        // Update the graph iframe with the new HTML content

        const graphIframe = document.getElementById('graph-iframe');
        graphIframe.srcdoc = data.graph_html;

        // Add the response to the chat window
        appendResponse(data.paragraph);
      })
      .catch(error => {
        console.error('Error:', error);
        // Handle errors if needed
      });
  }

  // Function to append user's question to the chat window
  function appendUserQuestion(question) {
    const chatWindow = document.getElementById('chat-window');
    const newQuestion = document.createElement('div');
    newQuestion.classList.add('chat-message');
    newQuestion.innerHTML = `<strong>User:</strong> ${question}`;
    chatWindow.appendChild(newQuestion);
  }

  // Function to append response to the chat window
  function appendResponse(response) {
    const chatWindow = document.getElementById('chat-window');
    const newResponse = document.createElement('div');
    newResponse.classList.add('chat-message');
    newResponse.innerHTML = `<strong>Bot:</strong> ${response}`;
    chatWindow.appendChild(newResponse);
  }

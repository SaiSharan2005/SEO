import React, { useState } from 'react';

const KeywordGeneration = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [keywords, setKeywords] = useState(null); // State to store generated keywords

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoFile(file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!videoFile) {
      alert('Please select a video file.');
      return;
    }

    setLoading(true);

    // Create form data to send to the server
    const formData = new FormData();
    formData.append('file', videoFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/keyword-with-keybert/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setKeywords(data.keywords); // Store the keywords from the response
        alert('Keywords generated successfully!');
      } else {
        alert(data.error || 'Failed to generate keywords.');
      }
    } catch (error) {
      console.error('Error during the request:', error);
      alert('An error occurred while processing the video.');
    }

    setLoading(false);
    setVideoFile(null);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-800">Keyword Generation</h1>
          <p className="mt-2 text-gray-600">Generate SEO keywords using AI-driven tools like KeyBERT.</p>
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-10">
        <section className="text-center">
          <h2 className="text-2xl font-semibold text-gray-800">Input your video to generate keywords</h2>
          <form onSubmit={handleSubmit} className="mt-6">
            <div className="mb-4">
              <input
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                className="border border-gray-300 rounded-md p-2 w-full"
              />
            </div>

            <button
              type="submit"
              className="mt-4 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-500"
              disabled={loading} // Disable the button while loading
            >
              {loading ? 'Processing...' : 'Generate Keywords'}
            </button>
          </form>

          {loading && (
            <p className="mt-4 text-yellow-600">Please wait while we process your video...</p>
          )}

          {/* Display generated keywords with their scores */}
          {keywords && (
            <div className="mt-6 text-left">
              <h3 className="text-lg font-bold text-gray-800">Generated Keywords:</h3>
              <ul className="list-disc list-inside text-gray-600">
                {keywords.map((keywordData, index) => (
                  <li key={index}>
                    <span className="font-semibold">{keywordData[0]}</span> - Score: {keywordData[1].toFixed(4)}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </main>

      <footer className="bg-gray-800 py-6">
        <div className="container mx-auto text-center text-gray-300">
          <p>&copy; 2024 SEO Video Processing. All Rights Reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default KeywordGeneration;

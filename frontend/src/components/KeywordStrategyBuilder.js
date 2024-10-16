import React, { useState } from 'react';

const KeywordStrategyBuilder = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [keywords, setKeywords] = useState(''); // State to hold the keywords input
  const [loading, setLoading] = useState(false); // State to manage loading status
  const [generatedKeywords, setGeneratedKeywords] = useState([]); // State to store generated keywords
  const [error, setError] = useState(''); // State to handle error messages

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoFile(file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); // Set loading to true on form submission
    setError(''); // Reset error state
    setGeneratedKeywords([]); // Reset the generated keywords

    // Prepare the form data for submission
    const formData = new FormData();
    formData.append('file', videoFile);
    formData.append('seed_keywords', keywords); // Pass the keywords as form data

    try {
      // Make the actual API call to your backend
      const response = await fetch('http://localhost:8000/keyword-with-keybert-seed/', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setGeneratedKeywords(result.keywords); // Store generated keywords in state
      } else {
        setError(result.error || 'An error occurred during processing.');
      }
    } catch (error) {
      console.error('Error while uploading:', error);
      setError('An error occurred while uploading the video.');
    }

    setLoading(false); // Set loading to false after processing
    setVideoFile(null); // Reset video file after processing
    setKeywords(''); // Reset keywords after processing
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-800">Keyword Strategy Builder</h1>
          <p className="mt-2 text-gray-600">Build a strong SEO strategy by analyzing keyword performance.</p>
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-10">
        <section className="text-center">
          <h2 className="text-2xl font-semibold text-gray-800">Plan Your Keyword Strategy</h2>
          <form onSubmit={handleSubmit} className="mt-6">
            {/* Keyword input */}
            <div className="mb-4">
              <textarea
                className="w-full p-4 border border-gray-300 rounded-md mb-4"
                placeholder="Enter keywords separated by spaces..."
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
              ></textarea>
              <p className="text-gray-600 text-sm">
                Keywords entered: {keywords ? keywords.split(' ').map(word => <span key={word} className="text-blue-600 mx-1">{word}</span>) : 'None'}
              </p>
            </div>

            {/* File input */}
            <div className="mb-4">
              <input
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                className="border border-gray-300 rounded-md p-2 w-full"
              />
            </div>

            {/* Submit button */}
            <button
              type="submit"
              className="mt-4 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-500"
              disabled={loading} // Disable the button while loading
            >
              {loading ? 'Processing...' : 'Submit Strategy'}
            </button>
          </form>

          {/* Inform the user to wait while processing */}
          {loading && (
            <p className="mt-4 text-yellow-600">Please wait while we process your video and keywords...</p>
          )}

          {/* Display error message if any */}
          {error && (
            <p className="mt-4 text-red-600">Error: {error}</p>
          )}

          {/* Display generated keywords */}
          {generatedKeywords.length > 0 && (
            <div className="mt-6">
              <h3 className="text-xl font-semibold text-gray-800">Generated Keywords:</h3>
              <ul className="mt-2 list-disc list-inside">
                {generatedKeywords.map((keyword, index) => (
                  <li key={index} className="text-gray-700">{keyword}</li>
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

export default KeywordStrategyBuilder;

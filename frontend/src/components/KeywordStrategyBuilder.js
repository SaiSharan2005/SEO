// src/components/KeywordStrategyBuilder.js
import React, { useState } from 'react';

const KeywordStrategyBuilder = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false); // State to manage loading status

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoFile(file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); // Set loading to true on form submission

    // Prepare the form data for submission
    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('content', content);

    // Simulate sending data to the server (Replace this with actual API call)
    console.log('Sending data to server:', formData);
    
    // Simulate a delay for processing (Replace this with actual upload logic)
    await new Promise((resolve) => setTimeout(resolve, 3000));

    setLoading(false); // Set loading to false after processing
    alert('Data sent to server and processing is finished.'); // Notify the user
    setVideoFile(null); // Reset video file after processing
    setContent(''); // Reset content after processing
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
            <textarea
              className="w-full h-40 p-4 border border-gray-300 rounded-md mb-4"
              placeholder="Enter your keyword strategy content here..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>

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
              {loading ? 'Processing...' : 'Submit Strategy'}
            </button>
          </form>

          {/* Inform the user to wait while processing */}
          {loading && (
            <p className="mt-4 text-yellow-600">Please wait while we process your video and content...</p>
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

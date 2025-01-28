import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom"; // Import Link for routing
import axios from "axios";

const Home = ({ isDarkMode }) => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/summarized-news"
        );
        setArticles(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching articles:", error);
      }
    };

    fetchArticles();
  }, []);

  if (loading) {
    return <p>Loading articles...</p>;
  }

  return (
    <div className="min-h-screen bg-white-50 font-sans">
      {/* Main Content */}
      <main className="px-5 py-10 lg:px-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          {/* Left Section */}
          <section className="lg:col-span-2">
            <h1 className="text-3xl font-bold lg:text-4xl">
              Most <span className="text-yellow-500">Sensational</span> News of
              The Week
            </h1>
            <p
              className={`mt-2 ${
                isDarkMode ? "text-gray-300" : "text-gray-600"
              }`}
            >
              Various events that became the main news headlines during the week
              and became the subject of discussion throughout the week.
            </p>
            <div className="mt-5 relative">
              <img
                src="https://api.time.com/wp-content/uploads/2015/04/nepal-earthquake-3.jpg"
                alt="Main Story"
                className="w-full rounded-lg"
              />
              <div className="absolute top-4 left-4 bg-yellow-500 text-white px-3 py-1 text-sm font-bold rounded-lg">
                MAIN STORY
              </div>
              <div className="absolute bottom-4 left-4 text-white">
                <h3 className="text-lg font-bold lg:text-2xl">
                  Earthquake in Nepal 2026 Lorem ipsum dolor sit amet
                  consectetur adipisicing elit. Ad, dolorem.
                </h3>
                <p className="text-sm mt-1 hidden md:block">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>
                <p className="mt-2 text-sm">
                  By <span className="font-medium">Samantha</span> and{" "}
                  <span className="font-medium">William</span> - 23 minutes ago
                </p>
              </div>
            </div>
          </section>

          {/* Right Section */}
          <aside className="mt-10">
            <h2 className="text-2xl font-bold mb-5">Latest News</h2>
            <div className="space-y-5">
              {articles.slice(0, 5).map((news, index) => (
                <div key={index} className="flex space-x-4">
                  <img
                    src={news.image}
                    alt={news.original_id}
                    className="w-20 h-20 object-cover rounded-lg sm:w-24 sm:h-24"
                  />
                  <div>
                    <p className="text-sm text-gray-500">{news.date}</p>
                    <h3 className="text-sm font-medium sm:text-lg">
                      {news.title}
                    </h3>
                    <p className="text-xs text-gray-500 mt-1 sm:text-sm">
                      By <span className="font-medium">Samantha</span> and{" "}
                      <span className="font-medium">William</span> - 23 minutes
                      ago
                    </p>

                    {/* Link to Title.jsx with passed article data */}
                    <Link

                      to={`/news/${news.original_id}`} // Dynamic route
                      state={{ news }} // Pass the state directly here
                    >
                      <p className="text-blue-500">Read More</p>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
};

export default Home;

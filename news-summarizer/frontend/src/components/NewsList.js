import React, { useEffect, useState } from "react";
import { fetchNews } from "../services/api";

const NewsList = () => {
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetchNews().then(setNews);
  }, []);

  return (
    <div>
      <h1>Summarized News</h1>
      {news.map((article, index) => (
        <div key={index}>
          <h2>{article.title}</h2>
          <p><strong>Summary:</strong> {article.summary}</p>
          <a href={article.url} target="_blank" rel="noopener noreferrer">Read More</a>
        </div>
      ))}
    </div>
  );
};

export default NewsList;

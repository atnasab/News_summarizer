export const fetchNews = async () => {
  const response = await fetch("http://127.0.0.1:5000/news");
  const data = await response.json();
  return data;
};

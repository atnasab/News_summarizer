import React from 'react'
import pic from "../../public/images/news.jpeg";

function Home() {
  return (
    
    <div className='max-w-screen-2xl  w-[50%] ml-[25%] '>
        <img className="md:w-[600px] md:h-[300px] ml-[80px] mt-5"
        src={pic} alt="News" />

        {/* Text Start */}
        <div className='w-[75%] ml-[90px] text-justify'>
        <h1 className='text-xl font-bold'>Viswanathan Anand predicted 99.73% draw, 0.27% Gukesh win an hour before Ding's blunder</h1> 
        <br />
        <p>An hour before the final game of World Chess Championship 2024 ended, five-time world chess champion Viswanathan Anand predicted a 99.73% chance of the game ending in a draw and a 0.27% chance of Gukesh D winning. However, later in the match, Ding Liren blundered, leading to Gukesh winning the game. Gukesh became the youngest world chess champion at 18.</p>
        {/* Text end */}
        </div>
    </div>
  )
}

export default Home
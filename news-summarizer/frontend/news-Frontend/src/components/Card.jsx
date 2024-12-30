import React from 'react';

function Card() {
  // console.log(data);

 

  // Conditional rendering if data is null or undefined
  // if (!data || data.length === 0) {
  //   return <div>No data available</div>;
  // }
 

  return (
    <div className='flex flex-wrap gap-5 justify-center bg-blue-100 p-[100px]'>
      {/* {data.map((currentData, index) => ( */}
        <div
           // Use a unique identifier if available, such as currentData.id
          className='bg-white w-[300px] p-5 shadow rounded-lg flex flex-col items-center'
        >
          <img
            src=''// Fallback image if urlToImage is missing
            alt="News Thumbnail"
            className='w-full h-[150px] object-cover rounded'
          />
          <div className='mt-3 text-center'>
            <a className='text-lg font-bold text-blue-600 hover:underline'>
              nsdms,
            </a>
            <p className='text-sm text-gray-600 mt-2'>
              hjss ddnks cklsm
            </p>
            <button 
            className='bg-blue-500 text-white py-1 px-3 rounded mt-3 hover:bg-blue-700'>
              Read More
            </button>
          </div>
        </div>
    </div>
  );
}

export default Card;

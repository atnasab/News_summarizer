import React from 'react'
import { FaFacebook,FaTwitter,FaInstagram,FaLinkedin } from 'react-icons/fa'

function Footer() {
  return (
   <>
   <hr />
   <footer className='py-12 bg-gray-800 text-white' >
    <div className='max-w-screen-2xl container mx-auto px-4 md:px-20' >
        <div className='flex flex-col size={24} items-center justify-center'>
            <div className='flex space-x-4'>
                <FaFacebook size={24}/>
                <FaTwitter size={24}/>
                <FaInstagram size={24}/>
                <FaLinkedin size={24}/>
            </div>
            <div className='mt-8 border-t border-gray-700 pt-8 flex flex-col  item-center'>
                <p>&copy; 2024 News <span className='text-red-700'>Web</span>. All rights reserved.</p>
            </div>
        </div>

    </div>
   </footer>
   </>
  )
}

export default Footer
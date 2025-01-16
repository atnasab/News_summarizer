import React from "react";
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from "react-icons/fa";

function Footer({ isDarkMode }) {
  return (
    <footer className={`py-12 ${isDarkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-black"} shadow-2xl border-t border-gray-700 `}>
        
      <div className="max-w-screen-2xl container mx-auto px-4 md:px-20">
        <div className="flex flex-col items-center justify-center">
          <div className="flex space-x-4">
            <FaFacebook size={24} />
            <FaTwitter size={24} />
            <FaInstagram size={24} />
            <FaLinkedin size={24} />
          </div>
          <div className="mt-8 border-t border-gray-700 pt-8 text-center">
            <p>&copy; 2024 News <span className="text-red-700">Web</span>. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;

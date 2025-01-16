import React from "react";
import { IoSearch } from "react-icons/io5";
import { MdDarkMode, MdLightMode } from "react-icons/md";
import { FaUser, FaBars, FaTimes } from "react-icons/fa";
import { useState } from "react";

function Navbar({ isDarkMode, setIsDarkMode }) {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleSearch = () => setIsSearchOpen((prev) => !prev);
  const toggleMenu = () => setIsMenuOpen((prev) => !prev);
  const toggleDarkMode = () => setIsDarkMode((prev) => !prev);

  return (
    <div
      className={`transition-colors duration-300 ${
        isDarkMode ? "bg-gray-900 text-white" : "bg-white text-black"
      }`}
    >
      <nav className="shadow-md px-4 py-5 flex justify-between items-center font-sans">
        {/* Logo */}
        <h1 className="text-2xl font-bold">
          News <span className="text-blue-600">Web</span>
        </h1>

        {/* Desktop Menu */}
        <ul className="hidden md:flex items-center space-x-7">
          {[
            "Entertainment",
            "Technology",
            "Politics",
            "Business",
            "Science",
            "Sports",
          ].map((item, index) => (
            <li
              key={index}
              className="hover:underline hover:text-blue-600 transition-colors"
            >
              <a href="#">{item}</a>
            </li>
          ))}
        </ul>

        {/* Icons Section */}
        <div className="flex gap-5 items-center">
          {/* Search Icon */}
          <div className="relative">
            <button
              onClick={toggleSearch}
              className="text-xl hover:text-blue-600 transition-colors mt-2"
            >
              <IoSearch />
            </button>
            <input
              type="text"
              placeholder="Search..."
              className={`absolute right-0 top-14 w-40 bg-gray-700 text-white px-4 py-1 rounded-md transition-transform duration-300 ${
                isSearchOpen ? "transform scale-100" : "transform scale-0"
              }`}
            />
          </div>

          {/* Dark Mode Toggle */}
          <button
            onClick={toggleDarkMode}
            className="text-xl hover:text-blue-600 transition-colors"
          >
            {isDarkMode ? <MdLightMode /> : <MdDarkMode />}
          </button>

          {/* User Icon */}

          <FaUser className="hover:text-blue-600 transition-colors cursor-pointer" />

          {/* Mobile Menu Toggle */}
          <button onClick={toggleMenu} className="md:hidden text-xl">
            {isMenuOpen ? <FaTimes /> : <FaBars />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div
        className={`fixed top-16 left-0 w-2/3 h-full z-10 transform transition-transform duration-300 md:hidden ${
          isMenuOpen ? "translate-x-0" : "-translate-x-full"
        } ${
          isDarkMode ? "bg-gray-900 text-white" : "bg-white text-black"
        } shadow-lg`}
      >
        <ul className="space-y-6 p-5 font-serif text-lg">
          {[
            "Entertainment",
            "Technology",
            "Politics",
            "Business",
            "Science",
            "Sports",
          ].map((item, index) => (
            <li key={index}>
              <a href="#" className="hover:text-blue-400 transition-colors">
                {item}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Navbar;

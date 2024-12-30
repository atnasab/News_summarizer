import React, { useState } from 'react';
import { FaBars } from "react-icons/fa";
import { IoSearch } from "react-icons/io5";
import Card from './Card';

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);

  return (
    <>
    <nav className="bg-gray-800 text-white px-4 py-5">
      <div className="flex items-center justify-between">
        {/* Toggle Icon (Mobile) */}
        <button
          className="md:hidden text-xl fo"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <FaBars/>
        </button>

        {/* Logo */}
        <div className="text-xl font-bold md:mx-4 ">
          <h1>News <span className='text-red-700'>Web</span></h1>
        </div>

        {/* Menu (Desktop) */}
        <ul
          className={`absolute md:relative md:flex md:items-center md:gap-5 transition-all duration-300 bg-gray-800 md:bg-transparent md:w-auto w-full left-0 ${
            menuOpen ? 'top-12' : '-top-full'
          }`}
        >
          <li>
            <a href="#" className="block py-2 md:py-0 px-4 hover:text-gray-400">
            Entertainment
            </a>
          </li>
          <li>
            <a href="#" className="block py-2 md:py-0 px-4 hover:text-gray-400">
            Technology
            </a>
          </li>
          <li>
            <a href="#" className="block py-2 md:py-0 px-4 hover:text-gray-400">
              Politics
            </a>
          </li>
          <li>
            <a href="#" className="block py-2 md:py-0 px-4 hover:text-gray-400">
            Business
            </a>
          </li>
          <li>
            <a href="#" className="block py-2 md:py-0 px-4 hover:text-gray-400">
            Science
            </a>
          </li>
          <li>
            <a href="#" className="block py-2 md:py-0 px-4 hover:text-gray-400">
            Sport
            </a>
          </li>
          
        </ul>

        {/* Search Icon */}
        <div className="relative flex items-center">
          <button
            className="text-xl md:mx-4"
            onClick={() => setSearchOpen(!searchOpen)}
          >
            <IoSearch />

          </button>

          {/* Search Input */}
          <input
            type="text"
            placeholder="Search..."
            className={`absolute right-0 top-12 md:top-12 md:right-4 md:absolute w-40 md:w-48 bg-gray-700 text-white px-4 py-1 rounded-md transition-all duration-300 ${
              searchOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
            }`}
          />
        </div>
      </div>
    </nav>
    <div>
      < Card />
     
    </div>
    </>
  );
};

export default Navbar;

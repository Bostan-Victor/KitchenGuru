import React from "react";
import Button from "./Button/Button";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";

function Navbar() {
  const navigate = useNavigate();
  const handleLogin = () => {
    navigate("/login");
  };
  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <>
      <div className="fixed top-[1%] left-[2%]">
        <img src={logo} className="w-[50%]"></img>
      </div>
      <div className="flex justify-between items-center font-main-font fixed top-[3%] left-[-1%] right-[-1%] mx-auto z-10 px-4 md:px-8 lg:max-w-7xl lg:px-0">
        <div className="text-2xl font-bold">
          <a href="/">Kitchen Guru</a>
        </div>
        <ul className="hidden md:flex gap-8 lg:gap-16 text-lg md:text-xl font-main-font text-black no-underline">
          <li>
            <a href="/Test">AI Recipe</a>
          </li>
          <li>
            <a href="/Test">Best 100</a>
          </li>
          <li>
            <a href="/AboutUs">About us</a>
          </li>
        </ul>
        <div className="flex gap-4 md:gap-8">
          <Button
            style="bg-33B249 text-white px-2 md:px-4 py-1 rounded-lg cursor-pointer transition duration-1000 hover:bg-black"
            onClick={handleLogin}
          >
            Login
          </Button>
          <Button
            style="bg-33B249 text-white px-2 md:px-4 py-1 rounded-lg cursor-pointer transition duration-1000 hover:bg-black"
            onClick={handleRegister}
          >
            Register
          </Button>
        </div>
      </div>
    </>
  );
}

export default Navbar;

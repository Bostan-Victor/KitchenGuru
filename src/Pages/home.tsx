import React from "react";
import fork from "../assets/bg.png";
import plate from "../assets/homapageplate.png";
import Navbar from "../Components/Navbar";
import ready from "../assets/ready_to_cook.png";
import Button from "../Components/Button/Button";
import { Navigate, useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();
  const MainPage = () => {
    navigate("/main");
  };
  const handleRecipe = () => { navigate("/recipe") }
  return (
    <>
      <Navbar />
      <div className="h-screen flex justify-center items-center transform">
        <div className=" w-[44.2%] h-[78%] bg-33B249 opacity-50 rounded-custom1">
          <img src={fork} className="absolute object-cover w-[44.2%] h-[78%]" />
        </div>
        <div className=" flex items-center justify-center w-[44.2%] h-[78%] bg-33B249 opacity-80 rounded-custom1">
          <img src={fork} className="absolute object-cover w-[44.2%] h-[78%]" />
        </div>
        <div className="absolute top-[25%] right-[63.5%] w-full text-right ">
          <div className="text-black font-main-font text-3xl whitespace-pre">
            <h1>Lack of imagination?</h1>
            <h1 className="mb-16">Want to try new food?</h1>
            <h1>Welcome to the best cooking</h1>
            <h1 className="mb-16">site for the best cooks!</h1>
            <h1>Here you can find over</h1>
            <h1>13000+ recipes</h1>
          </div>
        </div>
        <div className="absolute top-[28%] right-[-1%] w-full flex justify-center">
          <img src={plate} className="w-[28%]" />
        </div>
        <div className="fix absolute top-[38%] left-[50%] text-left">
          <img src={ready} className="w-[80%]"></img>
        </div>
        <Button
          style="absolute top-[73%] right-[64%] text-xl uppercase py-[1.6%] px-[5%] rounded-full transition font-main-font duration-500 text-white bg-black hover:bg-33B249 hover:text-black animate-bounce"
          onClick={MainPage}
        >
          Lets Cook
        </Button>
        <button className="absolute top-[70%] right-[58%] text-xl uppercase py-6 px-16 rounded-full transition font-main-font duration-500 text-white bg-black hover:bg-33B249 hover:text-black"onClick={handleRecipe}> Let's cook!</button>
      </div>
    </>
  );
}

export default HomePage;
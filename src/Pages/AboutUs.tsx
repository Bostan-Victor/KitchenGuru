import React from "react";
import Navbar from "../Components/Navbar";
import general from "../assets/category/general.jpg"

export default function AboutUs() {
  return (
    <div className="font-main-font">
      <Navbar />
      <div className="w-[30%] h-[15%] text-center text-xl absolute top-[15%] left-[34%]">
        <span className="text-6xl">About us</span>
        <span className="line-clamp-4">
          Recipes are like a map, guiding us through the flavors, textures, and
          traditions of the world.
        </span>
      </div>
      <div className="w-full h-[48%] absolute top-[35%] bg-[#33B249]">
        <div className="w-[38%] absolute top-[20%] left-[8%] text-center">
          <span className="text-6xl ">Our Mission</span>
          <span className="line-clamp-none text-xl text-justify"> 
            One of the most iconic forms of coking is grilling, where food is
            placed directly over an open flame or hot coals. This method imparts
            a smoky, charred flavor to ingredients like meat, vegetables, and
            even fruits. The sizzle of food hitting the grill and the
            tantalizing aroma of smoke wafting through the air create an
            irresistible sensory experience.
          </span>
        </div>
        <div className="border-4 w-[38%] h-full absolute top-[5%] right-[8%]">
          <img src={general} className="w-[200px] h-[200px]"></img>
        </div>
      </div>
    </div>
  );
}

import React, { useState } from "react";
import Navbar from "../Components/Navbar";
import Image from "../Components/Image/Image";
import profile from "../assets/profile_icon.png";
import Button from "../Components/Button/Button";
import { useNavigate } from "react-router-dom";
import "../index.css";
import general from "../assets/category/general.jpg";
import dessert from "../assets/category/dessert.jpeg";
import salads from "../assets/category/salads.jpeg";
import drinks from "../assets/category/drinks.jpeg";
import fast_food from "../assets/category/fast_food.jpeg";
import soups from "../assets/category/soups.png";
import meat from "../assets/category/meat.jpg";
import seafood from "../assets/category/seafood.jpeg";
import Inputbox from "../Components/Inputbox/Inputbox";

export default function MainPage() {
  const [data, setData] = useState<any[]>([]);
  const dd: any[] = [
    { id: 1, name: "mehuineaat" },
    { id: 2, name: "mehuineaat2" },
  ];
  const navigate = useNavigate();
  const ProfilePage = () => {
    navigate("/profile");
  };
  return (
    <div className="flex">
      <Navbar />
      <Button style="fixed top-[10%] right-[5%]" onClick={ProfilePage}>
        <img src={profile}></img>
      </Button>
      <div className="relative h-screen">
        <div className="w-[740px] flex h-[680px] content-center justify-center relative m-[100px] ">
          {!data.length ? (
            <>
              <span className="absolute top-[19%] left-[32%] text-2xl font-main-font 	">
                Select your category:
              </span>
              <Button onClick={() => console.log("seafood")}>
                <Image
                  url={seafood}
                  style="w-[120px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-30 ease-in-out absolute top-[27%] left-[20%] drop-shadow-2xl"
                ></Image>
              </Button>
              <Button onClick={() => console.log("general")}>
                <Image
                  url={general}
                  style="w-[270px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-30 ease-in-out absolute top-[37%] left-[31%] drop-shadow-2xl"
                ></Image>
              </Button>
              <Button onClick={() => setData([...dd])}>
                <Image
                  url={meat}
                  style="w-[160px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-30 ease-in-out absolute top-[68%] left-[16%] drop-shadow-2xl"
                ></Image>
              </Button>
              <Button onClick={() => console.log("salads")}>
                <Image
                  url={salads}
                  style="w-[110px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-30 ease-in-out absolute top-[28%] left-[62%] drop-shadow-2xl"
                ></Image>
              </Button>
              <Button onClick={() => console.log("soups")}>
                <Image
                  url={soups}
                  style="w-[200px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-30 ease-in-out absolute top-[41%] left-[0%] drop-shadow-2xl"
                ></Image>
              </Button>
              <Button onClick={() => console.log("dessert")}>
                <Image
                  url={dessert}
                  style="w-[160px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-1500 ease-in-out absolute top-[68%] left-[61%] drop-shadow-2xl"
                ></Image>
              </Button>
              <Image
                onClick={() => console.log("fast_food")}
                url={fast_food}
                style="w-[190px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-30 ease-in-out absolute top-[41%] left-[71%] drop-shadow-2xl"
              />
              <Button onClick={() => console.log("driks")}>
                <Image
                  url={drinks}
                  style="w-[120px] rounded-full scale-1 hover:scale-150 z-[0] hover:z-[999] transition duration-30 ease-in-out absolute top-[79%] left-[42%] drop-shadow-2xl"
                ></Image>
              </Button>
            </>
          ) : (
            <div>{data.map((el: any) => el.name)}</div>
          )}
        </div>
      </div>
      <div className="w-[550px] h-[auto]">
        <span className="absolute top-[26%] text-2xl font-main-font">
          Choose your ingredients:
        </span>
        <Inputbox
          name="Search here"
          style="flex w-[300px] px-[13px] py-[0.3%] my-4 border-2 border-black rounded-full absolute top-[30%]"
        ></Inputbox>
        <span className="absolute top-[39%] text-2xl font-main-font">
          Selected:
        </span>
      </div>
    </div>
  );
}
